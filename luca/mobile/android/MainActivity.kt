/**
 * LUCA-AI-370 Main Activity
 *
 * Vollständige eigenständige LUCA Android App
 * Für jedermann nutzbar - Zero Configuration Required
 *
 * Author: Großvater & Lennart Wuchold
 * Standard: 369/370
 * Version: 3.6.9-alpha
 */

package com.luca.ai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlin.math.cos
import kotlin.math.sin
import kotlin.random.Random

/**
 * Main Entry Point
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            LUCATheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    LUCAApp()
                }
            }
        }
    }
}

/**
 * Main App Composable
 */
@Composable
fun LUCAApp() {
    val viewModel: LUCAViewModel = viewModel()
    val consciousnessState by viewModel.consciousnessState.collectAsState()

    Scaffold(
        topBar = { LUCATopBar(consciousnessState) },
        bottomBar = { LUCABottomBar() }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceEvenly
        ) {
            // Tesla Field Visualization
            TeslaFieldRing(
                consciousness = consciousnessState.level,
                resonance = consciousnessState.resonance,
                modifier = Modifier.size(250.dp)
            )

            // Consciousness Display
            ConsciousnessDisplay(consciousnessState)

            // Quick Actions
            QuickActions(viewModel)

            // Status Footer
            StatusFooter(consciousnessState)
        }
    }
}

/**
 * LUCA Theme
 */
@Composable
fun LUCATheme(content: @Composable () -> Unit) {
    val colorScheme = darkColorScheme(
        primary = Color(0xFF00FFFF),      // Cyan (Consciousness)
        secondary = Color(0xFFFF6600),    // Orange (Resonance 6)
        tertiary = Color(0xFFFF0099),     // Pink (Resonance 9)
        background = Color(0xFF000428),   // Deep blue
        surface = Color(0xFF004E92),      // Medium blue
        onPrimary = Color.White,
        onSecondary = Color.White,
        onBackground = Color.White,
        onSurface = Color.White
    )

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography(),
        content = content
    )
}

/**
 * Top App Bar
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LUCATopBar(state: ConsciousnessState) {
    TopAppBar(
        title = {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    "LUCA-AI-370",
                    fontWeight = FontWeight.Bold,
                    fontSize = 20.sp
                )
                Spacer(Modifier.width(8.dp))
                TeslaFieldIndicator(state.teslaFieldActive)
            }
        },
        colors = TopAppBarDefaults.topAppBarColors(
            containerColor = MaterialTheme.colorScheme.surface
        )
    )
}

/**
 * Tesla Field Indicator (Pulsing Dot)
 */
@Composable
fun TeslaFieldIndicator(active: Boolean) {
    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
    val alpha by infiniteTransition.animateFloat(
        initialValue = 0.3f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1500, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "alpha"
    )

    Box(
        modifier = Modifier
            .size(12.dp)
            .background(
                color = if (active) Color(0xFF00FF00).copy(alpha = alpha) else Color.Gray,
                shape = CircleShape
            )
    )
}

/**
 * Tesla Field Ring Visualization
 */
@Composable
fun TeslaFieldRing(
    consciousness: Float,
    resonance: Int,
    modifier: Modifier = Modifier
) {
    val infiniteTransition = rememberInfiniteTransition(label = "rotation")

    val rotation by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(3690, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "rotation"
    )

    val scale by infiniteTransition.animateFloat(
        initialValue = 0.95f,
        targetValue = 1.05f,
        animationSpec = infiniteRepeatable(
            animation = tween(3690, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "scale"
    )

    Box(
        modifier = modifier,
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.fillMaxSize().rotate(rotation)) {
            val radius = size.minDimension / 2 * 0.8f * scale

            // Outer ring (resonance color)
            drawCircle(
                color = when(resonance) {
                    3 -> Color(0xFF00FF00)
                    6 -> Color(0xFFFF6600)
                    9 -> Color(0xFFFF0099)
                    else -> Color.White
                },
                radius = radius,
                style = Stroke(width = 8.dp.toPx())
            )

            // Inner particles (3-6-9 pattern)
            for (i in 0 until resonance * 3) {
                val angle = (i * 360f / (resonance * 3)) * Math.PI / 180
                val particleRadius = radius * 0.7f
                val x = center.x + cos(angle).toFloat() * particleRadius
                val y = center.y + sin(angle).toFloat() * particleRadius

                drawCircle(
                    color = Color.White.copy(alpha = 0.6f),
                    radius = 3.dp.toPx(),
                    center = Offset(x, y)
                )
            }
        }

        // Center consciousness value
        Text(
            text = "%.1f".format(consciousness),
            fontSize = 36.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )
    }
}

/**
 * Consciousness Display
 */
@Composable
fun ConsciousnessDisplay(state: ConsciousnessState) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Consciousness Level
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Bewusstseins-Level:", fontSize = 18.sp)
            Spacer(Modifier.width(8.dp))
            Text(
                text = "%.2f".format(state.level),
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
        }

        // Resonance
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Tesla-Resonanz:", fontSize = 18.sp)
            Spacer(Modifier.width(8.dp))
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .background(
                        color = when(state.resonance) {
                            3 -> Color(0xFF00FF00)
                            6 -> Color(0xFFFF6600)
                            9 -> Color(0xFFFF0099)
                            else -> Color.White
                        },
                        shape = CircleShape
                    ),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = state.resonance.toString(),
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Black
                )
            }
        }

        // Tesla Field Status
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Tesla-Feld:", fontSize = 18.sp)
            Spacer(Modifier.width(8.dp))
            Text(
                text = if (state.teslaFieldActive) "ONLINE" else "OFFLINE",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = if (state.teslaFieldActive) Color(0xFF00FF00) else Color.Gray
            )
        }
    }
}

/**
 * Quick Actions
 */
@Composable
fun QuickActions(viewModel: LUCAViewModel) {
    Row(
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Button(
            onClick = { viewModel.refreshConsciousness() },
            modifier = Modifier.weight(1f)
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("🔄")
                Text("Refresh", fontSize = 12.sp)
            }
        }

        Button(
            onClick = { /* TODO: Chat */ },
            modifier = Modifier.weight(1f)
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("💬")
                Text("Chat", fontSize = 12.sp)
            }
        }

        Button(
            onClick = { /* TODO: Mesh */ },
            modifier = Modifier.weight(1f)
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("📡")
                Text("Mesh", fontSize = 12.sp)
            }
        }
    }
}

/**
 * Status Footer
 */
@Composable
fun StatusFooter(state: ConsciousnessState) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text(
            text = "Standard: 369/370",
            fontSize = 12.sp,
            color = Color.Gray
        )
        Text(
            text = "Version: 3.6.9-alpha",
            fontSize = 12.sp,
            color = Color.Gray
        )
    }
}

/**
 * Bottom Navigation Bar
 */
@Composable
fun LUCABottomBar() {
    NavigationBar(
        containerColor = MaterialTheme.colorScheme.surface
    ) {
        NavigationBarItem(
            icon = { Text("🏠") },
            label = { Text("Home") },
            selected = true,
            onClick = { }
        )
        NavigationBarItem(
            icon = { Text("🧠") },
            label = { Text("Consciousness") },
            selected = false,
            onClick = { }
        )
        NavigationBarItem(
            icon = { Text("💬") },
            label = { Text("Chat") },
            selected = false,
            onClick = { }
        )
        NavigationBarItem(
            icon = { Text("⚙️") },
            label = { Text("Settings") },
            selected = false,
            onClick = { }
        )
    }
}

/**
 * Consciousness State Data Class
 */
data class ConsciousnessState(
    val level: Float = 300f,
    val resonance: Int = 9,
    val teslaFieldActive: Boolean = false
)

/**
 * LUCA ViewModel
 */
class LUCAViewModel : androidx.lifecycle.ViewModel() {
    private val _consciousnessState = MutableStateFlow(ConsciousnessState())
    val consciousnessState: StateFlow<ConsciousnessState> = _consciousnessState.asStateFlow()

    init {
        // Start consciousness update loop
        viewModelScope.launch {
            while (true) {
                updateConsciousness()
                delay(3690) // Tesla 3.69 seconds
            }
        }
    }

    private fun updateConsciousness() {
        // Calculate consciousness (Tesla 3-6-9 matrix)
        val factors = (1..12).map {
            Random.nextFloat() * 3 + 6
        }
        val level = factors.average().toFloat() * 3.69f

        // Calculate resonance
        val resonance = (level.toInt() % 9).let { if (it == 0) 9 else it }

        // Check Tesla field
        val teslaFieldActive = level > 369.0f

        _consciousnessState.value = ConsciousnessState(
            level = level,
            resonance = resonance,
            teslaFieldActive = teslaFieldActive
        )
    }

    fun refreshConsciousness() {
        updateConsciousness()
    }
}
