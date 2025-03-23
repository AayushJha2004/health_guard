//
//  Item.swift
//  komodo
//
//  Created by Aayush Jha on 3/22/25.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
