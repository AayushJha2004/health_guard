import SwiftUI
import SwiftData

struct ContentView: View {
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Top Header Section
                HeaderView()

                // Vitals Grid
                VitalsGridView()

                // Call Doctor & Health Alerts Row
                HStack {
                    // "Call Your Doctor" button
                    Button(action: {
                        print("Calling your doctor...")
                    }) {
                        HStack {
                            Image(systemName: "phone.fill")
                            Text("Call Your Doctor")
                                .fontWeight(.semibold)
                        }
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                    }

                    Spacer()

                    // Health Alerts Button
                    Button(action: {
                        print("Health alerts tapped")
                    }) {
                        VStack {
                            Image(systemName: "exclamationmark.triangle.fill")
                                .font(.largeTitle)
                                .foregroundColor(.red)
                            Text("Your Health Alerts")
                                .fontWeight(.bold)
                                .font(.footnote)
                        }
                    }
                    Spacer()
                }
                .padding()

                // "Your Doctor" title + Doctor Info Button
                VStack(alignment: .leading, spacing: 8) {
                    Text("Your Doctor")
                        .font(.title3)
                        .fontWeight(.bold)
                        .padding(.leading)
                    
                    DoctorInfoButton()
                }

                Spacer()

                // Bottom Navigation Row
                BottomNavigationView()
            }
            .navigationBarHidden(true)
            .onAppear {
                print("ContentView appeared.")
                HealthKitManager.shared.requestAuthorization()
            }
        }
    }
}

// MARK: - Header Section
struct HeaderView: View {
    var body: some View {
        ZStack(alignment: .bottomLeading) {
            Color.blue
                .edgesIgnoringSafeArea(.top)
                .frame(height: 140)
            
            HStack(alignment: .center) {
                Image("profileImage")
                    .resizable()
                    .frame(width: 60, height: 60)
                    .clipShape(Circle())
                    .padding(.leading)
                
                VStack(alignment: .leading) {
                    Text("Welcome")
                        .font(.subheadline)
                        .foregroundColor(.white)
                    Text("Aayush Jha")
                        .font(.title3)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                }
                .padding(.leading, 8)
                
                Spacer()
            }
            .padding(.bottom, 8)
        }
    }
}

// MARK: - Vitals Section
struct VitalsGridView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Your Vitals")
                .font(.title3)
                .fontWeight(.bold)
                .padding(.leading)
            
            HStack {
                VitalButton(iconName: "bed.double.fill", title: "Sleep") {
                    print("Sleep tapped")
                }
                VitalButton(iconName: "wind", title: "Respiration") {
                    print("Respiration tapped")
                }
                VitalButton(iconName: "heart.fill", title: "Heart Rate") {
                    print("Heart Rate tapped")
                }
            }
            .padding(.horizontal)
            
            HStack {
                VitalButton(iconName: "thermometer", title: "Body Temp") {
                    print("Body Temp tapped")
                }
                VitalButton(iconName: "waveform.path.ecg", title: "ECG") {
                    print("ECG tapped")
                }
            }
            .padding(.horizontal)
        }
        .padding(.top)
    }
}

// MARK: - Vital Button (as Button)
struct VitalButton: View {
    var iconName: String
    var title: String
    var action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack {
                Image(systemName: iconName)
                    .font(.system(size: 36))
                    .foregroundColor(.purple)
                Text(title)
                    .font(.footnote)
                    .foregroundColor(.gray)
                    .multilineTextAlignment(.center)
            }
            .frame(maxWidth: .infinity)
            .padding()
            .background(Color.white)
            .cornerRadius(10)
            .shadow(color: Color.black.opacity(0.1), radius: 4, x: 0, y: 2)
        }
    }
}

// MARK: - Doctor Info Section (as Button)
struct DoctorInfoButton: View {
    var body: some View {
        Button(action: {
            print("Doctor info tapped")
        }) {
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Image("doctorImage")
                        .resizable()
                        .clipShape(Circle())
                        .frame(width: 60, height: 60)
                    
                    VStack(alignment: .leading) {
                        Text("Dr. Manoj Nath Yogi")
                            .font(.headline)
                        Text("Consultant - Internal Medicine")
                            .font(.subheadline)
                            .foregroundColor(.gray)
                    }
                    Spacer()
                }
                
                HStack {
                    Image(systemName: "star.fill")
                        .foregroundColor(.yellow)
                    Text("4.9 (57 Reviews)")
                        .font(.subheadline)
                        .foregroundColor(.gray)
                }
            }
            .padding()
            .background(Color.white)
            .cornerRadius(10)
            .shadow(color: Color.black.opacity(0.1), radius: 4, x: 0, y: 2)
            .padding(.horizontal)
        }
    }
}

// MARK: - Bottom Navigation
struct BottomNavigationView: View {
    var body: some View {
        HStack {
            Spacer()
            NavButton(icon: "house.fill", label: "Home") {
                print("Home tapped")
            }
            Spacer()
            NavButton(icon: "stethoscope", label: "Doctors") {
                print("Doctors tapped")
            }
            Spacer()
            NavButton(icon: "heart.text.square.fill", label: "Vitals") {
                print("Vitals tapped")
            }
            Spacer()
            NavButton(icon: "person.fill", label: "Profile") {
                print("Profile tapped")
            }
            Spacer()
        }
        .padding(.vertical, 10)
        .background(Color.white)
        .cornerRadius(20, corners: [.topLeft, .topRight])
        .shadow(color: Color.black.opacity(0.1), radius: 4, x: 0, y: -2)
    }
}

struct NavButton: View {
    var icon: String
    var label: String
    var action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack {
                Image(systemName: icon)
                    .font(.system(size: 22))
                Text(label)
                    .font(.caption2)
            }
            .foregroundColor(.blue)
        }
    }
}

// MARK: - Rounded Corner Helper
extension View {
    func cornerRadius(_ radius: CGFloat, corners: UIRectCorner) -> some View {
        clipShape(RoundedCorner(radius: radius, corners: corners))
    }
}

struct RoundedCorner: Shape {
    var radius: CGFloat = 0.0
    var corners: UIRectCorner = .allCorners
    
    func path(in rect: CGRect) -> Path {
        let path = UIBezierPath(
            roundedRect: rect,
            byRoundingCorners: corners,
            cornerRadii: CGSize(width: radius, height: radius)
        )
        return Path(path.cgPath)
    }
}

#Preview {
    ContentView()
        .modelContainer(for: Item.self, inMemory: true)
}
