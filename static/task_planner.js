document.addEventListener("DOMContentLoaded", () => {
  const generateBtn = document.querySelector(".generate-btn");
  const textArea = document.getElementById("taskText");
  const fileInput = document.getElementById("fileUpload");
  const output = document.getElementById("taskPlannerOutput");

  generateBtn.addEventListener("click", async () => {
    let text = textArea.value.trim();

    // If no text, try file upload
    if (!text && fileInput.files.length > 0) {
      const file = fileInput.files[0];
      const reader = new FileReader();

      if (file.type === "text/plain") {
        reader.onload = async function () {
          const fileText = reader.result;
          await processText(fileText);
        };
        reader.readAsText(file);
      } else if (file.type === "application/pdf") {
        reader.onload = async function () {
          const typedArray = new Uint8Array(reader.result);
          const pdfjsLib = window["pdfjs-dist/build/pdf"];
          pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js";

          const pdf = await pdfjsLib.getDocument(typedArray).promise;
          let textContent = "";

          for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const content = await page.getTextContent();
            const strings = content.items.map(item => item.str).join(" ");
            textContent += strings + "\n";
          }

          await processText(textContent);
        };
        reader.readAsArrayBuffer(file);
      } else {
        output.innerHTML = "<p>❌ Unsupported file type. Please upload a PDF or TXT file.</p>";
      }

    } else if (text) {
      await processText(text);
    } else {
      output.innerHTML = "<p>⚠️ Please enter text or upload a file.</p>";
    }
  });

  async function processText(inputText) {
    output.innerHTML = "<p>⏳ Generating your plan...</p>";

    try {
      const response = await fetch("/task_planner", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText }),
      });

      const result = await response.json();
      output.innerHTML = `<pre>${result.result}</pre>`;
    } catch (err) {
      output.innerHTML = "<p>❌ Something went wrong. Please try again.</p>";
      console.error(err);
    }
  }
});
