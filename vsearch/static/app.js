const form = document.querySelector("form");
const vectorOutput = document.getElementById("vector");
const colbertOutput = document.getElementById("colbert");
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  vectorOutput.innerHTML = "<progress />";
  colbertOutput.innerHTML = "<progress />";
  const formData = new FormData(form);
  fetch("/vector", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      vectorOutput.innerHTML = parseContent(data[0]);
    });
  fetch("/colbert", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      colbertOutput.innerHTML = parseContent(data[0]);
    });
});

function parseContent(content) {
  return content
    .split("\n")
    .map((line) => `<p>${line.trim()}</p>`)
    .join("");
}
