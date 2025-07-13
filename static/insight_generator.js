async function callInsightGenerator() {
  const fileInput = document.getElementById("file-upload");
  if (!fileInput.files[0]) {
    alert("Please select a file.");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const res = await fetch("/insight_generator", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();

  const result = document.getElementById("insight-result");
  if (data.error) {
    result.innerHTML = data.error;
  } else {
    result.innerHTML = data.result;

    const chartSection = document.querySelector(".charts");
    chartSection.innerHTML = "";
    data.charts.forEach(url => {
      const img = document.createElement("img");
      img.src = url;
      img.width = 200;
      chartSection.appendChild(img);
    });
  }
}

function downloadCharts() {
  window.location.href = "/download_charts";
}
