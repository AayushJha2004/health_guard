import HealthKit
import Foundation

class HealthKitManager {
    static let shared = HealthKitManager()
    private let healthStore = HKHealthStore()
    
    // Global storage for data from heart rate, respiratory rate, and body temperature fetches.
    private var dataToSend: [[String: Any]] = []
    // Single timer that synchronizes the three fetches.
    private var syncTimer: Timer?
    
    // Request HealthKit authorization for heart rate, ECG, respiratory rate, body temperature, and sleep analysis data.
    func requestAuthorization() {
        guard HKHealthStore.isHealthDataAvailable() else { return }
        
        // Heart rate is a quantity type.
        guard let heartRateType = HKObjectType.quantityType(forIdentifier: .heartRate) else { return }
        // ECG is non-optional.
        let ecgType = HKObjectType.electrocardiogramType()
        // Respiratory rate is a quantity type.
        guard let respiratoryRateType = HKObjectType.quantityType(forIdentifier: .respiratoryRate) else { return }
        // Body temperature (wrist temperature) – using a custom identifier.
        guard let bodyTemperatureType = HKObjectType.quantityType(forIdentifier: .appleSleepingWristTemperature) else { return }
        // Sleep analysis is a category type.
        guard let sleepType = HKObjectType.categoryType(forIdentifier: .sleepAnalysis) else { return }
        
        // Request read access for all types.
        healthStore.requestAuthorization(toShare: [],
                                         read: [heartRateType, ecgType, respiratoryRateType, bodyTemperatureType, sleepType]) { success, error in
            if success {
                print("HealthKit authorization granted for all requested data.")
                // Start timer-based fetches for heart rate, respiratory rate, and body temperature.
                self.startSynchronizedTimer()
                // Start observer queries for ECG and sleep analysis.
                self.startECGObserverQuery()
                self.startSleepObserverQuery()
            } else {
                print("Authorization failed: \(error?.localizedDescription ?? "No error info")")
            }
        }
    }
    
    // MARK: - Synchronized Timer for HR, RR, and Body Temperature
    
    /// Starts a single timer that fires every 60 seconds to run all three fetches.
    func startSynchronizedTimer() {
        // Invalidate any existing timer.
        syncTimer?.invalidate()
        DispatchQueue.main.async { [weak self] in
            self?.syncTimer = Timer.scheduledTimer(withTimeInterval: 30.0, repeats: true) { _ in
                // Trigger each fetch.
                self?.fetchLatestHeartRateData()
                self?.fetchLatestRespiratoryRateData()
                self?.fetchLatestBodyTemperatureData()
                
                // Wait a few seconds to allow asynchronous queries to finish,
                // then flush the accumulated data.
                DispatchQueue.main.asyncAfter(deadline: .now() + 5) {
                    self?.flushDataToServer()
                }
            }
        }
        print("Synchronized timer started for heart rate, respiratory rate, and body temperature.")
    }
    
    /// Flush the accumulated data to the server and then clear the data array.
    func flushDataToServer() {
        guard !dataToSend.isEmpty else {
            print("No data to send.")
            return
        }
        print("Flushing accumulated data:")
        for datum in dataToSend {
            print(datum)
        }
        // Send all accumulated data in one HTTP POST request.
        sendDataToServer(data: dataToSend)
        // Clear the array after sending.
        dataToSend.removeAll()
    }
    
    // MARK: - Heart Rate: Timer-Based Fetch (appends to global dataToSend)
    
    func fetchLatestHeartRateData() {
        guard let heartRateType = HKObjectType.quantityType(forIdentifier: .heartRate) else { return }
        let sortDescriptor = NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: false)
        
        let heartRateQuery = HKSampleQuery(sampleType: heartRateType,
                                           predicate: nil,
                                           limit: 10,
                                           sortDescriptors: [sortDescriptor]) { [weak self] query, results, error in
            guard let samples = results as? [HKQuantitySample], error == nil else {
                print("Error fetching heart rate samples: \(error?.localizedDescription ?? "Unknown error")")
                return
            }
            
            let heartRateUnit = HKUnit.count().unitDivided(by: HKUnit.minute())
            for sample in samples {
                let heartRate = sample.quantity.doubleValue(for: heartRateUnit)
                let sampleData: [String: Any] = [
                    "heartRate": heartRate,
                    "timestamp": sample.startDate.timeIntervalSince1970
                ]
                self?.dataToSend.append(sampleData)
            }
            print("Fetched and appended heart rate data.")
        }
        healthStore.execute(heartRateQuery)
    }
    
    // MARK: - Respiratory Rate: Timer-Based Fetch (appends to global dataToSend)
    
    func fetchLatestRespiratoryRateData() {
        guard let respiratoryRateType = HKObjectType.quantityType(forIdentifier: .respiratoryRate) else { return }
        let sortDescriptor = NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: false)
        
        let respiratoryRateQuery = HKSampleQuery(sampleType: respiratoryRateType,
                                                 predicate: nil,
                                                 limit: 10,
                                                 sortDescriptors: [sortDescriptor]) { [weak self] query, results, error in
            guard let samples = results as? [HKQuantitySample], error == nil else {
                print("Error fetching respiratory rate samples: \(error?.localizedDescription ?? "Unknown error")")
                return
            }
            
            let respiratoryRateUnit = HKUnit.count().unitDivided(by: HKUnit.minute())
            for sample in samples {
                let respiratoryRate = sample.quantity.doubleValue(for: respiratoryRateUnit)
                let sampleData: [String: Any] = [
                    "respiratoryRate": respiratoryRate,
                    "timestamp": sample.startDate.timeIntervalSince1970
                ]
                self?.dataToSend.append(sampleData)
            }
            print("Fetched and appended respiratory rate data.")
        }
        healthStore.execute(respiratoryRateQuery)
    }
    
    // MARK: - Body Temperature: Timer-Based Fetch (appends to global dataToSend)
    
    func fetchLatestBodyTemperatureData() {
        guard let bodyTemperatureType = HKObjectType.quantityType(forIdentifier: .appleSleepingWristTemperature) else { return }
        let sortDescriptor = NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: false)
        
        let temperatureQuery = HKSampleQuery(sampleType: bodyTemperatureType,
                                             predicate: nil,
                                             limit: 10,
                                             sortDescriptors: [sortDescriptor]) { [weak self] query, results, error in
            guard let samples = results as? [HKQuantitySample], error == nil else {
                print("Error fetching body temperature samples: \(error?.localizedDescription ?? "Unknown error")")
                return
            }
            
            let temperatureUnit = HKUnit.degreeCelsius()
            for sample in samples {
                let temperature = sample.quantity.doubleValue(for: temperatureUnit)
                let sampleData: [String: Any] = [
                    "bodyTemperature": temperature,
                    "timestamp": sample.startDate.timeIntervalSince1970
                ]
                self?.dataToSend.append(sampleData)
            }
            print("Fetched and appended body temperature data.")
        }
        healthStore.execute(temperatureQuery)
    }
    
    // MARK: - ECG Observer & Fetch (Observer Query Remains)
    
    func startECGObserverQuery() {
        let ecgType = HKObjectType.electrocardiogramType()
        
        let ecgObserver = HKObserverQuery(sampleType: ecgType, predicate: nil) { [weak self] query, completionHandler, error in
            if let error = error {
                print("ECG observer query error: \(error.localizedDescription)")
                return
            }
            self?.fetchLatestECGData()
            completionHandler()
        }
        healthStore.execute(ecgObserver)
        print("ECG observer query started.")
    }
    
    func fetchLatestECGData() {
        let ecgType = HKObjectType.electrocardiogramType()
        
        let ecgQuery = HKSampleQuery(sampleType: ecgType,
                                     predicate: nil,
                                     limit: HKObjectQueryNoLimit,
                                     sortDescriptors: nil) { [weak self] query, samples, error in
            if let error = error {
                print("Error fetching ECG samples: \(error.localizedDescription)")
                return
            }
            
            guard let ecgSamples = samples as? [HKElectrocardiogram] else {
                print("Unable to convert samples to [HKElectrocardiogram]")
                return
            }
            
            var dataToSendECG: [[String: Any]] = []
            let dispatchGroup = DispatchGroup()
            
            for sample in ecgSamples {
                dispatchGroup.enter()
                var measurementsArray = [[String: Any]]()
                
                let voltageQuery = HKElectrocardiogramQuery(sample) { (query, result) in
                    switch result {
                    case .measurement(let measurement):
                        if let voltageQuantity = measurement.quantity(for: HKElectrocardiogram.Lead.appleWatchSimilarToLeadI) {
                            let voltage = voltageQuantity.doubleValue(for: HKUnit.volt())
                            let measurementData: [String: Any] = [
                                "voltage": voltage,
                                "timeSinceSampleStart": measurement.timeSinceSampleStart
                            ]
                            measurementsArray.append(measurementData)
                        }
                    case .done:
                        print("Done retrieving voltage measurements for sample at \(sample.startDate)")
                        let frequencyValue = sample.samplingFrequency?.doubleValue(for: HKUnit.hertz()) ?? 0.0
                        let sampleData: [String: Any] = [
                            "ecgStartDate": sample.startDate.timeIntervalSince1970,
                            "samplingFrequency": frequencyValue,
                            "numberOfVoltageMeasurements": sample.numberOfVoltageMeasurements,
                            "voltageMeasurements": measurementsArray
                        ]
                        dataToSendECG.append(sampleData)
                        dispatchGroup.leave()
                    case .error(let error):
                        print("Error retrieving voltage measurements: \(error.localizedDescription)")
                        dispatchGroup.leave()
                    }
                }
                self?.healthStore.execute(voltageQuery)
            }
            
            dispatchGroup.notify(queue: .main) {
//                print("ECG Data:")
//                for data in dataToSendECG {
//                    print(data)
//                }
//                self?.sendDataToServerStatic(data: dataToSendECG)
            }
        }
        
        healthStore.execute(ecgQuery)
    }
    
    // MARK: - Sleep Analysis Observer & Fetch (Observer Query Remains)
    
    func startSleepObserverQuery() {
        guard let sleepType = HKObjectType.categoryType(forIdentifier: .sleepAnalysis) else { return }
        
        let sleepObserver = HKObserverQuery(sampleType: sleepType, predicate: nil) { [weak self] query, completionHandler, error in
            if let error = error {
                print("Sleep analysis observer query error: \(error.localizedDescription)")
                return
            }
            self?.fetchLatestSleepData()
            completionHandler()
        }
        healthStore.execute(sleepObserver)
        print("Sleep analysis observer query started.")
    }
    
    func fetchLatestSleepData() {
        guard let sleepType = HKObjectType.categoryType(forIdentifier: .sleepAnalysis) else {
            print("Sleep analysis type not available.")
            return
        }
        
        let startDate = Calendar.current.date(byAdding: .day, value: -7, to: Date())
        let predicate = HKQuery.predicateForSamples(withStart: startDate, end: Date(), options: [])
        let sortDescriptor = NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: true)
        
        let sleepQuery = HKSampleQuery(sampleType: sleepType,
                                       predicate: predicate,
                                       limit: HKObjectQueryNoLimit,
                                       sortDescriptors: [sortDescriptor]) { query, results, error in
            if let error = error {
                print("Error fetching sleep data: \(error.localizedDescription)")
                return
            }
            
            guard let sleepSamples = results as? [HKCategorySample] else {
                print("Unable to convert sleep data to HKCategorySample")
                return
            }
            
            var aggregatedDurations: [String: TimeInterval] = [
                "inBed": 0,
                "awake": 0,
                "core": 0,
                "deep": 0,
                "rem": 0,
                "unspecified": 0
            ]
            
            for sample in sleepSamples {
                let duration = sample.endDate.timeIntervalSince(sample.startDate)
                if let sleepValue = HKCategoryValueSleepAnalysis(rawValue: sample.value) {
                    switch sleepValue {
                    case .awake:
                        aggregatedDurations["awake"]! += duration
                    case .asleepCore:
                        aggregatedDurations["core"]! += duration
                    case .asleepDeep:
                        aggregatedDurations["deep"]! += duration
                    case .asleepREM:
                        aggregatedDurations["rem"]! += duration
                    case .asleepUnspecified:
                        aggregatedDurations["unspecified"]! += duration
                    @unknown default:
                        aggregatedDurations["unspecified"]! += duration
                    }
                } else {
                    aggregatedDurations["unspecified"]! += duration
                }
            }
            
            aggregatedDurations["inBed"] = (aggregatedDurations["awake"] ?? 0) +
                                           (aggregatedDurations["core"] ?? 0) +
                                           (aggregatedDurations["deep"] ?? 0) +
                                           (aggregatedDurations["rem"] ?? 0)
            
            var earliestDate: Date?
            var latestDate: Date?
            for sample in sleepSamples {
                let sampleStart = sample.startDate
                if earliestDate == nil || sampleStart < earliestDate! {
                    earliestDate = sampleStart
                }
                if latestDate == nil || sampleStart > latestDate! {
                    latestDate = sampleStart
                }
            }
            
            let startTimestamp = earliestDate?.timeIntervalSince1970 ?? 0
            let endTimestamp = latestDate?.timeIntervalSince1970 ?? 0
            print("Earliest sample date: \(startTimestamp)")
            print("Latest sample date: \(endTimestamp)")
            
            var dataToSendSleep: [[String: Any]] = []
            var aggregatedDurationsInHours: [String: Double] = [:]
            for (stage, duration) in aggregatedDurations {
                aggregatedDurationsInHours[stage] = duration / 3600.0
                let sampleData: [String: Any] = [
                    stage: aggregatedDurationsInHours[stage] ?? 0,
                    "timestamp": startTimestamp
                ]
                dataToSendSleep.append(sampleData)
            }
            
            print("Aggregated Sleep Data (in hours):")
            for (stage, hours) in aggregatedDurationsInHours {
                print("\(stage): \(hours) hours")
            }
            
            self.sendDataToServerStatic(data: dataToSendSleep)
        }
        
        healthStore.execute(sleepQuery)
    }
    
    // MARK: - Data Transmission
    
    func sendDataToServer(data: [[String: Any]]) {
        guard let url = URL(string: "http://10.23.112.46:8000/api/data") else {
            print("Server not found")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: data, options: [])
            request.httpBody = jsonData
            if let jsonString = String(data: jsonData, encoding: .utf8) {
                print("Data to be sent: \(jsonString)")
            }
        } catch {
            print("Error serializing JSON: \(error.localizedDescription)")
            return
        }
        
        let task = URLSession.shared.dataTask(with: request) { responseData, response, error in
            if let error = error {
                print("Error sending data: \(error.localizedDescription)")
                return
            }
            
            if let httpResponse = response as? HTTPURLResponse {
                print("HTTP Response Status Code: \(httpResponse.statusCode)")
            }
            
            if let data = responseData, let responseString = String(data: data, encoding: .utf8) {
                print("Response Data: \(responseString)")
            } else {
                print("No response data received.")
            }
            
            print("Data sent successfully!")
        }
        task.resume()
    }
    
    func sendDataToServerStatic(data: [[String: Any]]) {
        guard let url = URL(string: "http://10.23.112.46:8000/api/static") else {
            print("Server not found")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: data, options: [])
            request.httpBody = jsonData
            if let jsonString = String(data: jsonData, encoding: .utf8) {
                print("Data to be sent: \(jsonString)")
            }
        } catch {
            print("Error serializing JSON: \(error.localizedDescription)")
            return
        }
        
        let task = URLSession.shared.dataTask(with: request) { responseData, response, error in
            if let error = error {
                print("Error sending data: \(error.localizedDescription)")
                return
            }
            
            if let httpResponse = response as? HTTPURLResponse {
                print("HTTP Response Status Code: \(httpResponse.statusCode)")
            }
            
            if let data = responseData, let responseString = String(data: data, encoding: .utf8) {
                print("Response Data: \(responseString)")
            } else {
                print("No response data received.")
            }
            
            print("Data sent successfully!")
        }
        task.resume()
    }
}
