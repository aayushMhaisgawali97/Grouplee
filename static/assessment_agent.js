document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("assessmentForm");
  const fileInput = document.getElementById("fileInput");
  const textInput = document.getElementById("textInput");
  const difficulty = document.getElementById("difficulty");
  const questionsBox = document.getElementById("questions");
  const feedbackBox = document.getElementById("feedback");

  //  Format output for clean HTML display
  const formatOutput = (text) => {
    return text
      .replace(/(?:\r\n|\r|\n)/g, "<br>")  // Convert newlines to <br>
      .replace(/Answer:/gi, "<strong>Answer:</strong>")
      .replace(/Feedback:/gi, "<strong>Feedback:</strong>")
      .replace(/Questions:/gi, "<strong>Questions:</strong>");
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();
    if (fileInput.files.length > 0) {
      formData.append("file", fileInput.files[0]);
    }

    formData.append("text", textInput.value.trim());
    formData.append("difficulty", difficulty.value);

    questionsBox.innerHTML = "⏳ Generating questions...";
    feedbackBox.innerHTML = "⏳ Generating feedback...";

    try {
      const response = await fetch("/assessment_agent", {
        method: "POST",
        body: formData
      });

      const result = await response.json();

      if (result.error) {
        questionsBox.innerHTML = feedbackBox.innerHTML = `❌ ${result.error}`;
      } else {
        // ✅ Use formatted HTML output
        questionsBox.innerHTML = formatOutput(result.questions || "No questions generated.");
        feedbackBox.innerHTML = formatOutput(result.feedback || "No feedback generated.");
      }
    } catch (err) {
      questionsBox.innerHTML = feedbackBox.innerHTML = "❌ Something went wrong.";
      console.error(err);
    }
  });
});
