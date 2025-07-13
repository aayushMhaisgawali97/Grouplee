async function callContentGenerator() {
  const topic = document.getElementById('topic').value;
  const type = document.getElementById('type').value;

  if (!topic || !type) {
    alert("Please enter a topic and select a type.");
    return;
  }

  const res = await fetch('/content_generator', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ topic: topic, type: type })
  });

  if (!res.ok) {
    alert("Error generating content!");
    return;
  }

  if (type === "text") {
    const data = await res.json();
    document.getElementById('result').innerText = data.content || "No content generated.";
  } else {
    const blob = await res.blob();
    let filename = "output";

    const mime = res.headers.get('Content-Type');
    if (mime.includes("pdf")) filename += ".pdf";
    else if (mime.includes("presentation")) filename += ".pptx";
    else if (mime.includes("image")) filename += ".jpg";

    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
  }
}
