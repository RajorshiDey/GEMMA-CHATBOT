const message = document.getElementById("input")
const sendBtn = document.getElementById("send")

sendBtn.addEventListener("click", (e)=>{
    console.log(message.value);
    setBodyToMarkdownText(message.value);
    message.value = '';;
})



async function setBodyToMarkdownText(text){
    document.getElementById("output").innerHTML = "<p>⏳ Thinking...</p>";
    const response = await fetchResponse(text);
    const markdownText = `${response}`; 
    const html = marked.parse(markdownText);
    document.getElementById("output").classList.add("markdown-body")
    document.getElementById("output").innerHTML = html;
}

async function fetchResponse(input) {
    try {
        const response = await fetch("https://gemma-chatbot-backend.onrender.com/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                content: input   // must match your FastAPI Input model
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();
        return data.message;

    } catch (error) {
        console.error("Error fetching response:", error);
        return "Failed to fetch response";
    }
}