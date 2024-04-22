document.querySelectorAll('.lesson-btn').forEach(button => {
    button.addEventListener('click', function() {
        let content = this.nextElementSibling;
        this.classList.toggle('active');
        content.classList.toggle('active');

        if (content.classList.contains('active')) {
            content.style.maxHeight = content.scrollHeight + "px"; // Убираем эту строку
            this.querySelector('.arrow').textContent = '▲';
            updatePageHeight();
        } else {
            content.style.maxHeight = '0'; // Это достаточно для сворачивания контента
            this.querySelector('.arrow').textContent = '▼';
            updatePageHeight();
        }
    });
});

function updatePageHeight() {
    let newHeight = document.body.scrollHeight;
    document.querySelectorAll('.lesson-content.active').forEach(activeContent => {
        newHeight += activeContent.scrollHeight;
    });
    document.body.style.minHeight = `${newHeight}px`;
}

document.addEventListener('DOMContentLoaded', () => {
    updatePageHeight();
});
