document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("summarizerForm");
  const fileInput = document.getElementById("fileInput");
  const summaryResult = document.getElementById("summaryResult");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    summaryResult.innerText = "⏳ Generating summary...";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
      const response = await fetch("/summarize", {
        method: "POST",
        body: formData
      });

      const result = await response.json();

      if (result.error) {
        summaryResult.innerText = "❌ " + result.error;
      } else {
        summaryResult.innerText = result.summary;
      }
    } catch (err) {
      console.error(err);
      summaryResult.innerText = "❌ Failed to generate summary.";
    }
  });
});
