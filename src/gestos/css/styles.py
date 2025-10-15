"""
Configuración de estilos para la aplicación de gestos
Colores, fuentes, dimensiones y estilos de botones
"""

# Paleta de colores moderna
COLORS = {
    # Colores de fondo
    'bg_dark': '#0a0e27',
    'bg_medium': '#1a1f3a',
    'bg_light': '#2a2f4a',
    
    # Colores de texto
    'text_light': '#ffffff',
    'text_medium': '#b8c5d6',
    'text_dark': '#8892a6',
    
    # Colores de acento
    'accent_blue': '#3b82f6',
    'accent_purple': '#8b5cf6',
    'accent_cyan': '#06b6d4',
    'accent_neon': '#00ff88',
    
    # Colores de estado
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    
    # Efectos
    'shadow': '#000000',
    'border': '#4a5568',
}

# Configuración de fuentes
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'subtitle': ('Segoe UI', 14, 'bold'),
    'body': ('Segoe UI', 11),
    'button': ('Segoe UI', 11, 'bold'),
    'gesture': ('Segoe UI', 20, 'bold'),
    'small': ('Segoe UI', 9),
}

# Dimensiones de la interfaz
DIMENSIONS = {
    'window_width': 1200,
    'window_height': 800,
    'video_width': 640,
    'video_height': 480,
    'button_width': 15,
    'button_height': 2,
    'padding': 10,
    'border_width': 2,
}

# Estilos de botones
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['accent_blue'],
        'fg': COLORS['text_light'],
        'active_bg': COLORS['bg_medium'],
        'active_fg': COLORS['accent_blue'],
    },
    'success': {
        'bg': COLORS['success'],
        'fg': COLORS['text_light'],
        'active_bg': COLORS['bg_medium'],
        'active_fg': COLORS['success'],
    },
    'warning': {
        'bg': COLORS['warning'],
        'fg': COLORS['text_light'],
        'active_bg': COLORS['bg_medium'],
        'active_fg': COLORS['warning'],
    },
    'danger': {
        'bg': COLORS['danger'],
        'fg': COLORS['text_light'],
        'active_bg': COLORS['bg_medium'],
        'active_fg': COLORS['danger'],
    },
}
