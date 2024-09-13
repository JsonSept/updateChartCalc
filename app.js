// Function to calculate energy output and update charts
function fetchData() {
  // Fetch input values from the form
  const voltage = document.querySelector('select[name="voltage"]').value;
  const current = document.querySelector('select[name="current"]').value;
  const power = document.querySelector('select[name="power"]').value;
  const panelArea = document.querySelector('select[name="panel_area"]').value;
  const efficiency = document.querySelector('select[name="efficiency"]').value;
  const currencyRate = document.querySelector('input[name="currency_rate"]').value;
  const numPanels = document.querySelector('input[name="num_panels"]').value;
  const solarIrradiance = document.querySelector('input[name="solar_irradiance"]').value;
  const hoursOfSunlight = 6;  // For example, 6 hours of sunlight

  // Calculate output in Watts (P = Solar Irradiance * Panel Area * Efficiency)
  const outputWatts = solarIrradiance * panelArea * (efficiency / 100) * numPanels;

  // Convert to kWh (assuming output over one hour)
  let outputKWh = outputWatts / 1000 * hoursOfSunlight; // Assuming 1 hour of sunlight for now (or adjust for actual hours)

  // Calculate cost (kWh * currency rate)
  let totalCost = outputKWh * currencyRate;

  // Round off to 2 decimal places
  outputKWh = parseFloat(outputKWh.toFixed(2));
  totalCost = parseFloat(totalCost.toFixed(2));

  // Calculate grid connection metrics
  let energyExportedToGrid = outputKWh * 0.8; // Assuming 80% is exported to the grid
  let localConsumption = outputKWh * 0.2; // Assuming 20% is consumed locally
  energyExportedToGrid = parseFloat(energyExportedToGrid.toFixed(2))
  localConsumption = parseFloat(localConsumption.toFixed(2))
  // Update charts
  updateProductionChart(outputKWh, energyExportedToGrid, localConsumption);
  updateCostChart(totalCost);
  updateUsageEstimateChart(outputWatts);

  // Display results (optional as text)
  console.log(`Output (Watts): ${outputWatts}`);
  console.log(`Output (kWh): ${outputKWh}`);
  console.log(`Total Cost: R ${totalCost}`);
  console.log(`Energy Exported to Grid (kWh): ${energyExportedToGrid}`);
  console.log(`Local Consumption (kWh): ${localConsumption}`);

  document.getElementById('outputWattsText').innerText = `Output (Watts): ${outputWatts}`;
  document.getElementById('outputKWhText').innerText = `Output (kWh): ${outputKWh}`;
  document.getElementById('totalCostText').innerText = `Total Cost: R ${totalCost}`;
  document.getElementById('energyExportedText').innerText = `Energy Exported to Grid (kWh): ${energyExportedToGrid}`;
  document.getElementById('localConsumptionText').innerText = `Local Consumption (kWh): ${localConsumption}`;
}


// Chart update functions
function updateProductionChart(outputKWh) {
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
