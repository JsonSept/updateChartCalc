from flask import Flask, jsonify, render_template_string
import random
import time
from threading import Thread

app = Flask(__name__)

# Global variable to store the solar irradiance
current_irradiance = 200  # Initial value in W/m²

def update_solar_irradiance():
    global current_irradiance
    while True:
        # Simulate fluctuating solar irradiance based on random factors
        temperature_effect = random.uniform(-10, 10)
        current_irradiance = max(0, 200 + temperature_effect)  # Ensure it doesn't go below 0
        time.sleep(60)  # Update every 60 seconds

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Energy Calculator</title>
  <link rel="stylesheet" href="styles.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    function fetchData() {
      fetch('/solar-irradiance')
        .then(response => response.json())
        .then(data => {
          const solarIrradiance = data.solar_irradiance;

          // Fetch input values from the form
          const voltage = document.querySelector('select[name="voltage"]').value;
          const current = document.querySelector('select[name="current"]').value;
          const power = document.querySelector('select[name="power"]').value;
          const panelArea = document.querySelector('select[name="panel_area"]').value;
          const efficiency = document.querySelector('select[name="efficiency"]').value;
          const currencyRate = document.querySelector('input[name="currency_rate"]').value;
          const numPanels = document.querySelector('input[name="num_panels"]').value;
          const hoursOfSunlight = 6;  // For example, 6 hours of sunlight

          // Calculate output in Watts
          const outputWatts = solarIrradiance * panelArea * (efficiency / 100) * numPanels;

          // Convert to kWh
          let outputKWh = outputWatts / 1000 * hoursOfSunlight; // Assuming 1 hour of sunlight for now

          // Calculate cost
          let totalCost = outputKWh * currencyRate;

          // Round off to 2 decimal places
          outputKWh = parseFloat(outputKWh.toFixed(2));
          totalCost = parseFloat(totalCost.toFixed(2));

          // Calculate grid connection metrics
          const energyExportedToGrid = outputKWh * 0.8; // Assuming 80% is exported to the grid
          const localConsumption = outputKWh * 0.2; // Assuming 20% is consumed locally

          // Update charts
          updateProductionChart(outputKWh, energyExportedToGrid, localConsumption);
          updateCostChart(totalCost);
          updateUsageEstimateChart(outputWatts);

          // Display results
          document.getElementById('outputWattsText').innerText = `Output (Watts): ${outputWatts}`;
          document.getElementById('outputKWhText').innerText = `Output (kWh): ${outputKWh}`;
          document.getElementById('totalCostText').innerText = `Total Cost: R ${totalCost}`;
          document.getElementById('energyExportedText').innerText = `Energy Exported to Grid (kWh): ${energyExportedToGrid}`;
          document.getElementById('localConsumptionText').innerText = `Local Consumption (kWh): ${localConsumption}`;
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    }

    // Chart update functions
    function updateProductionChart(outputKWh, energyExportedToGrid, localConsumption) {
      const ctx = document.getElementById('productionChart').getContext('2d');
      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Produced kWh', 'Remaining'],
          datasets: [{
            data: [outputKWh, 24 - outputKWh], // Assuming a 24-hour day for reference
            backgroundColor: ['#4caf50', '#ccc'],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
        }
      });
    }

    function updateCostChart(totalCost) {
      const ctx = document.getElementById('costChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Cost (Currency)'],
          datasets: [{
            label: 'Cost (per day)',
            data: [totalCost],
            backgroundColor: ['#f44336'],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
        }
      });
    }

    function updateUsageEstimateChart(outputWatts) {
      const ctx = document.getElementById('usageChart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5'], // Example hours
          datasets: [{
            label: 'Usage (Watts)',
            data: [outputWatts, outputWatts * 0.8, outputWatts * 0.6, outputWatts * 0.5, outputWatts * 0.4], // Example usage pattern
            backgroundColor: 'rgba(66, 135, 245, 0.2)',
            borderColor: '#4287f5',
            fill: true,
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
        }
      });
    }

    // Call fetchData periodically
    setInterval(fetchData, 60000); // Update every 60 seconds
  </script>
</head>
<body>
  <div class="container">
    <div class="calculator">
      <h2>Energy Calculator</h2>
      <form id="energy-form">
        <label for="voltage">Voltage (V):</label>
        <select name="voltage" required>
          <option value="12">12V DC</option>
          <option value="24">24V DC</option>
          <option value="48">48V DC</option>
          <option value="96">96V DC</option>
          <option value="200">200V DC</option>
          <option value="400">400V DC</option>
          <option value="600">600V DC</option>
        </select>

        <label for="current">Current (A):</label>
        <select name="current" required>
          <option value="5">5A</option>
          <option value="10">10A</option>
          <option value="15">15A</option>
          <option value="20">20A</option>
          <option value="25">25A</option>
          <option value="30">30A</option>
          <option value="40">40A</option>
          <option value="50">50A</option>
        </select>

        <label for="power">Power (W):</label>
        <select name="power" required>
          <option value="1000">1 kW</option>
          <option value="2000">2 kW</option>
          <option value="3000">3 kW</option>
          <option value="5000">5 kW</option>
          <option value="10000">10 kW</option>
          <option value="15000">15 kW</option>
          <option value="20000">20 kW</option>
          <option value="30000">30 kW</option>
          <option value="50000">50 kW</option>
        </select>

        <label for="panel_area">Panel Area (m²):</label>
        <select name="panel_area" required>
          <option value="1">1 m²</option>
          <option value="2">2 m²</option>
          <option value="3">3 m²</option>
          <option value="5">5 m²</option>
          <option value="10">10 m²</option>
          <option value="20">20 m²</option>
          <option value="30">30 m²</option>
          <option value="50">50 m²</option>
          <option value="100">100 m²</option>
        </select>

        <label for="efficiency">Efficiency (%):</label>
        <select name="efficiency" required>
          <option value="15">15%</option>
          <option value="16">16%</option>
          <option value="17">17%</option>
          <option value="18">18%</option>
          <option value="19">19%</option>
          <option value="20">20%</option>
          <option value="21">21%</option>
          <option value="22">22%</option>
        </select>

        <label for="currency_rate">Currency Rate (per kWh):</label>
        <input type="number" step="0.01" name="currency_rate" required>

        <label for="num_panels">Number of Panels:</label>
        <input type="number" step="1" name="num_panels" required>

        <label for="solar_irradiance">Solar Irradiance (W/m²):</label>
        <input type="number" step="0.01" name="solar_irradiance" required>

        <button type="button" onclick="fetchData()">Fetch Data</button>
      </form>
    </div>
    <br>
    <div class="charts">
      <div>
        <h3>Production</h3>
        <canvas id="productionChart"></canvas>
      </div><br>
      <div>
        <h3>Cost</h3>
        <canvas id="costChart"></canvas>
      </div>
      <div>
        <h3>Usage Estimate</h3>
        <canvas id="usageChart"></canvas>
      </div>
    </div>
    <div id="results">
      <p id="outputWattsText"></p>
      <p id="outputKWhText"></p>
      <p id="totalCostText"></p>
      <p id="energyExportedText">Energy Exported to Grid (kWh): </p>
      <p id="localConsumptionText">Local Consumption (kWh): </p>
    </div>
  </div>
</body>
</html>
    ''')

@app.route('/solar-irradiance', methods=['GET'])
def get_solar_irradiance():
    return jsonify({'solar_irradiance': current_irradiance})

if __name__ == '__main__':
    # Start the background thread for updating solar irradiance
    Thread(target=update_solar_irradiance, daemon=True).start()
    app.run(debug=True)
