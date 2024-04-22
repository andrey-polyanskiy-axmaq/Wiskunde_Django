document.querySelectorAll('.lesson-btn').forEach(button => {
    button.addEventListener('click', function() {
        var content = this.nextElementSibling;
        this.classList.toggle('active');
        content.classList.toggle('active');

        if (content.classList.contains('active')) {
            content.style.maxHeight = content.scrollHeight + "px";
            this.querySelector('.arrow').textContent = '▲';
            updatePageHeight();
        } else {
            content.style.maxHeight = null;
            this.querySelector('.arrow').textContent = '▼';
            updatePageHeight();
        }
    });
});

function updatePageHeight() {
    // Начинаем с начальной высоты body, которая может быть установлена в вашем CSS
    let newHeight = document.body.scrollHeight;

    // Суммируем высоту всех открытых плашек
    document.querySelectorAll('.lesson-content.active').forEach(activeContent => {
        newHeight += activeContent.scrollHeight;
    });

    // Устанавливаем новую высоту для body
    document.body.style.minHeight = `${newHeight}px`;
}

// Устанавливаем начальное состояние высоты страницы при загрузке
document.addEventListener('DOMContentLoaded', () => {
    updatePageHeight();
});
