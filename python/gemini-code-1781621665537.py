import matplotlib.pyplot as plt
import re

def load_sound_data(filepath):
    """
    Liest die Modelldaten ein und bereinigt sie von 
    Inlinemarkern wie und Kommentaren.
    """
    heights, pressures, temps, dews, dirs, spds, rhs = [], [], [], [], [], [], []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Entfernt Quelltext-Marker wie \ mitten im Text
    cleaned_content = re.sub(r'\\', '', content)
    
    for line in cleaned_content.splitlines():
        line = line.strip()
        # Überspringe Header- und Kommentarzeilen
        if not line or line.startswith('#') or line.startswith('h('):
            continue
            
        parts = line.split()
        # Falls eine Zeile unvollständig ist (z.B. durch Zeilenumbruch getrennt)
        if len(parts) < 7:
            continue
            
        try:
            heights.append(float(parts[0]))
            pressures.append(float(parts[1]))
            temps.append(float(parts[2]))
            dews.append(float(parts[3]))
            dirs.append(float(parts[4]))
            spds.append(float(parts[5]))
            rhs.append(float(parts[6]))
        except ValueError:
            continue # Überspringe Zeilen, die sich nicht parsen lassen
            
    return {
        'h': heights, 'p': pressures, 'T': temps, 
        'Dew': dews, 'Dir': dirs, 'Spd': spds, 'RH': rhs
    }

# --- Daten laden ---
# Ersetze die Dateinamen falls deine Dateien lokal anders heißen
data1 = load_sound_data('2026-06-16_0000Z_ICON_D2_HEIDIS.txt')
data2 = load_sound_data('2026-06-16_0000Z_ICON-D2_Stiwoll.txt')

# --- Plot-Konfiguration ---
# Da Profile meist bis in die Stratosphäre gehen, begrenzen wir die 
# vertikale Achse standardmäßig auf die Troposphäre (z.B. 6000m oder 12000m), 
# um meteorologische Details am Boden besser zu erkennen.
MAX_ALTITUDE = 6000  # In Metern (AGL). Für volles Profil einfach auskommentieren.

fig, axs = plt.subplots(2, 3, figsize=(16, 10), sharey=True)
axs = axs.flatten()

# Definition der Plots: (Spaltenkey, Label, X-Achsen-Beschriftung, Farbe)
plots_config = [
    ('p', 'Druck', 'Druck (hPa)', 'grey'),
    ('T', 'Temperatur & Taupunkt', 'Temperatur (°C)', 'red'), # Taupunkt wird hier mitgeplottet
    ('RH', 'Relative Feuchte', 'Feuchtigkeit (%)', 'green'),
    ('Spd', 'Windgeschwindigkeit', 'Geschwindigkeit (m/s)', 'blue'),
    ('Dir', 'Windrichtung', 'Richtung (°)', 'orange')
]

for i, (key, title, xlabel, color) in enumerate(plots_config):
    ax = axs[i]
    
    if key == 'T':
        # Sonderfall: Temperatur UND Taupunkt in einem Diagramm
        ax.plot(data1['T'], data1['h'], label='T (Datei 1)', color='red', linestyle='-')
        ax.plot(data1['Dew'], data1['h'], label='Dew (Datei 1)', color='blue', linestyle='--')
        ax.plot(data2['T'], data2['h'], label='T (Datei 2)', color='darkred', linestyle=':')
        ax.plot(data2['Dew'], data2['h'], label='Dew (Datei 2)', color='darkblue', linestyle='-.')
        ax.legend(loc='lower left', fontsize='small')
    else:
        # Standardplot für die anderen Parameter
        ax.plot(data1[key], data1['h'], label='Datei 1', color=color, linestyle='-')
        ax.plot(data2[key], data2['h'], label='Datei 2', color=color, linestyle='--')
        ax.legend(loc='best', fontsize='small')
        
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel(xlabel)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    if MAX_ALTITUDE:
        ax.set_ylim(0, MAX_ALTITUDE)

# Die erste Achse bekommt die Y-Beschriftung (Höhe) für die Zeilen
axs[0].set_ylabel('Höhe (m AGL)', fontsize=11)
axs[3].set_ylabel('Höhe (m AGL)', fontsize=11)

# Das leere 6. Subplot-Feld verstecken
axs[5].axis('off')

plt.suptitle('Optischer Vergleich der ICON-D2 Profile (Stiwoll)', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()