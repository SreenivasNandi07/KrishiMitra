function showPanel(id) {
    document.querySelectorAll('.panel').forEach(p => {
        p.classList.add('hidden');
    });
    document.getElementById(id).classList.remove('hidden');
}
