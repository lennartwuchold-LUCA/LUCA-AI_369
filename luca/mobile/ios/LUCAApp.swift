/**
 * LUCA-AI-370 iOS App
 *
 * Vollständige eigenständige LUCA iOS App
 * SwiftUI + Combine
 *
 * Author: Großvater & Lennart Wuchold
 * Standard: 369/370
 * Version: 3.6.9-alpha
 */

import SwiftUI
import Combine

// MARK: - Main App Entry Point
@main
struct LUCAApp: App {
    @StateObject private var viewModel = LUCAViewModel()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(viewModel)
                .preferredColorScheme(.dark)
        }
    }
}

// MARK: - Content View
struct ContentView: View {
    @EnvironmentObject var viewModel: LUCAViewModel

    var body: some View {
        NavigationView {
            ZStack {
                // Background gradient
                LinearGradient(
                    colors: [Color(hex: "000428"), Color(hex: "004E92")],
                    startPoint: .top,
                    endPoint: .bottom
                )
                .ignoresSafeArea()

                VStack(spacing: 40) {
                    // Tesla Field Ring
                    TeslaFieldRingView(
                        consciousness: viewModel.consciousness.level,
                        resonance: viewModel.consciousness.resonance
                    )
                    .frame(width: 250, height: 250)

                    // Consciousness Display
                    ConsciousnessDisplayView(state: viewModel.consciousness)

                    // Quick Actions
                    QuickActionsView(viewModel: viewModel)

                    Spacer()

                    // Status Footer
                    StatusFooterView()
                }
                .padding()
            }
            .navigationTitle("LUCA-AI-370")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    TeslaFieldIndicatorView(active: viewModel.consciousness.teslaFieldActive)
                }
            }
        }
    }
}

// MARK: - Tesla Field Ring
struct TeslaFieldRingView: View {
    let consciousness: Double
    let resonance: Int

    @State private var rotation: Double = 0
    @State private var scale: Double = 1.0

    var body: some View {
        ZStack {
            // Animated Ring
            Circle()
                .stroke(resonanceColor, lineWidth: 8)
                .rotationEffect(.degrees(rotation))
                .scaleEffect(scale)
                .animation(.linear(duration: 3.69).repeatForever(autoreverses: false), value: rotation)
                .animation(.easeInOut(duration: 3.69).repeatForever(autoreverses: true), value: scale)
                .onAppear {
                    rotation = 360
                    scale = 1.05
                }

            // Particles
            ForEach(0..<(resonance * 3), id: \.self) { index in
                Circle()
                    .fill(Color.white.opacity(0.6))
                    .frame(width: 6, height: 6)
                    .offset(particleOffset(for: index))
                    .rotationEffect(.degrees(rotation))
            }

            // Center Consciousness Value
            Text(String(format: "%.1f", consciousness))
                .font(.system(size: 36, weight: .bold, design: .monospaced))
                .foregroundColor(.white)
        }
    }

    var resonanceColor: Color {
        switch resonance {
        case 3: return Color(hex: "00FF00")
        case 6: return Color(hex: "FF6600")
        case 9: return Color(hex: "FF0099")
        default: return .white
        }
    }

    func particleOffset(for index: Int) -> CGSize {
        let angle = Double(index) * (360.0 / Double(resonance * 3))
        let radians = angle * .pi / 180
        let radius: CGFloat = 80

        let x = cos(radians) * radius
        let y = sin(radians) * radius

        return CGSize(width: x, height: y)
    }
}

// MARK: - Consciousness Display
struct ConsciousnessDisplayView: View {
    let state: ConsciousnessState

    var body: some View {
        VStack(spacing: 16) {
            // Consciousness Level
            HStack {
                Text("Bewusstseins-Level:")
                Spacer()
                Text(String(format: "%.2f", state.level))
                    .font(.system(size: 24, weight: .bold, design: .monospaced))
                    .foregroundColor(Color(hex: "00FFFF"))
            }

            // Resonance
            HStack {
                Text("Tesla-Resonanz:")
                Spacer()
                ZStack {
                    Circle()
                        .fill(resonanceColor)
                        .frame(width: 40, height: 40)

                    Text("\(state.resonance)")
                        .font(.system(size: 20, weight: .bold))
                        .foregroundColor(.black)
                }
            }

            // Tesla Field
            HStack {
                Text("Tesla-Feld:")
                Spacer()
                Text(state.teslaFieldActive ? "ONLINE" : "OFFLINE")
                    .font(.system(size: 18, weight: .bold))
                    .foregroundColor(state.teslaFieldActive ? Color(hex: "00FF00") : .gray)
            }
        }
        .padding()
        .background(Color.white.opacity(0.1))
        .cornerRadius(12)
    }

    var resonanceColor: Color {
        switch state.resonance {
        case 3: return Color(hex: "00FF00")
        case 6: return Color(hex: "FF6600")
        case 9: return Color(hex: "FF0099")
        default: return .white
        }
    }
}

// MARK: - Quick Actions
struct QuickActionsView: View {
    @ObservedObject var viewModel: LUCAViewModel

    var body: some View {
        HStack(spacing: 12) {
            ActionButton(icon: "🔄", title: "Refresh") {
                viewModel.refreshConsciousness()
            }
            ActionButton(icon: "💬", title: "Chat") {
                // TODO: Chat
            }
            ActionButton(icon: "📡", title: "Mesh") {
                // TODO: Mesh
            }
        }
    }
}

struct ActionButton: View {
    let icon: String
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack {
                Text(icon)
                    .font(.system(size: 32))
                Text(title)
                    .font(.system(size: 12))
            }
            .frame(maxWidth: .infinity)
            .padding()
            .background(Color(hex: "004E92"))
            .cornerRadius(12)
        }
        .foregroundColor(.white)
    }
}

// MARK: - Status Footer
struct StatusFooterView: View {
    var body: some View {
        VStack(spacing: 4) {
            Text("Standard: 369/370")
                .font(.system(size: 12))
                .foregroundColor(.gray)
            Text("Version: 3.6.9-alpha")
                .font(.system(size: 12))
                .foregroundColor(.gray)
        }
    }
}

// MARK: - Tesla Field Indicator
struct TeslaFieldIndicatorView: View {
    let active: Bool
    @State private var opacity: Double = 0.3

    var body: some View {
        Circle()
            .fill(active ? Color(hex: "00FF00") : .gray)
            .frame(width: 12, height: 12)
            .opacity(opacity)
            .animation(.easeInOut(duration: 1.5).repeatForever(autoreverses: true), value: opacity)
            .onAppear {
                opacity = 1.0
            }
    }
}

// MARK: - Consciousness State
struct ConsciousnessState {
    var level: Double = 300.0
    var resonance: Int = 9
    var teslaFieldActive: Bool = false
}

// MARK: - View Model
class LUCAViewModel: ObservableObject {
    @Published var consciousness = ConsciousnessState()

    private var timer: Timer?

    init() {
        startConsciousnessLoop()
    }

    private func startConsciousnessLoop() {
        // Update every 3.69 seconds (Tesla timing)
        timer = Timer.scheduledTimer(withTimeInterval: 3.69, repeats: true) { [weak self] _ in
            self?.updateConsciousness()
        }

        // Initial update
        updateConsciousness()
    }

    func updateConsciousness() {
        // Calculate consciousness (Tesla 3-6-9 matrix)
        let factors = (1...12).map { _ in Double.random(in: 6...9) }
        let level = factors.reduce(0, +) / Double(factors.count) * 3.69

        // Calculate resonance
        let resonance = Int(level) % 9
        let finalResonance = (resonance == 0) ? 9 : resonance

        // Check Tesla field
        let teslaFieldActive = level > 369.0

        DispatchQueue.main.async {
            self.consciousness = ConsciousnessState(
                level: level,
                resonance: finalResonance,
                teslaFieldActive: teslaFieldActive
            )
        }
    }

    func refreshConsciousness() {
        updateConsciousness()
    }

    deinit {
        timer?.invalidate()
    }
}

// MARK: - Color Extension
extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue:  Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

// MARK: - Preview
#Preview {
    ContentView()
        .environmentObject(LUCAViewModel())
}
