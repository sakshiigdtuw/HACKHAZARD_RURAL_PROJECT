document
  .getElementById("language-select")
  .addEventListener("change", async function () {
    const targetLang = this.value;
    const elements = document.querySelectorAll(".translatable");

    for (const element of elements) {
      const originalText =
        element.getAttribute("data-original") || element.textContent;

      try {
        const translatedText =
          targetLang === "en"
            ? originalText // no translation needed
            : await translateText(originalText, "en", targetLang);

        // Store original English text once
        if (!element.getAttribute("data-original")) {
          element.setAttribute("data-original", originalText);
        }

        element.textContent = translatedText;
      } catch (error) {
        console.error("Translation error:", error);
      }
    }
  });

async function translateText(text, source, target) {
  const res = await fetch(
    `https://api.mymemory.translated.net/get?q=${encodeURIComponent(
      text
    )}&langpair=${source}|${target}`
  );

  const data = await res.json();
  return data.responseData.translatedText;
}
