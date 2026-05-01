document.addEventListener("DOMContentLoaded", e => {
    const suggestions = document.getElementById("suggestions");
    const queryInput = document.getElementById("query");
    const form = document.getElementById("search-form");
 
    queryInput.addEventListener("input", e => {
        let value = e.target.value.toLowerCase();
        for (let child of suggestions.children) {
            child.style.display = child.children[0].innerText.includes(value.toLowerCase()) ? "block" : "none";
        }
    });

    queryInput.addEventListener("keydown", e => {
        if (e.code == "Tab") {
            for (let child of suggestions.children) {
                if (child.style.display == "block") {
                    queryInput.value = child.children[0].innerText;
                    break;
                }
            }
        }
    });

    form.addEventListener("submit", e => {
        form.submit();
        form.reset();
        e.preventDefault();
    });
});