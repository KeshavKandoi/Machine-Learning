async function ask() {
  const question = document.getElementById("question").value.trim();
  const videoId = document.getElementById("video_id").value.trim();
  const responseEl = document.getElementById("response");

  if (!question || !videoId) {
    responseEl.textContent = "Please enter both a Video ID and a question.";
    return;
  }

  responseEl.textContent = "Thinking...";

  try {
    const res = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, video_id: videoId })
    });

    const data = await res.json();
    responseEl.textContent = data.answer ?? "No answer returned.";
  } catch (err) {
    responseEl.textContent = "Error: Could not reach the server.";
    console.error(err);
  }
}