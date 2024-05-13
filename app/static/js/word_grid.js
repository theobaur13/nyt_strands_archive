function render_word_grid(strand, letters) {
    const wordGrid = document.querySelector('.word-grid');
    const wordGridItems = letters.sort((a, b) => a.index - b.index).map(letter => {
        const div = document.createElement('div');
        div.classList.add('letter');
        div.id = `${letter.index}`;
        div.setAttribute('data-clickable', "False");
        div.textContent = letter.letter;
        return div;
    });

    wordGridItems.forEach(item => wordGrid.appendChild(item));
}

function get_adjacent_letters(letter, letters) {
    // Grid is 6 columns x 8 rows, index starts at 1
    const adjacentLetters = [];
    const index = parseInt(letter.index);
    const row = Math.floor(index / 6);
    const col = ((index - 1) % 6);

    // Check up-left
    if (row > 0 && col > 0) {
        let foundLetter = letters.find(l => l.index === index - 7);
        if (foundLetter) adjacentLetters.push(foundLetter);
    }

    // Check up
    if (row > 0) {
        let foundLetter = letters.find(l => l.index === index - 6);
        if (foundLetter) adjacentLetters.push(foundLetter);
    }

    // Check up-right
    if (row > 0 && col < 5) {
        let foundLetter = letters.find(l => l.index === index - 5);
        if (foundLetter) adjacentLetters.push(foundLetter);
    }

    // Check left
    if (col > 0) {
        let foundLetter = letters.find(l => l.index === index - 1);
        if (foundLetter) adjacentLetters.push(foundLetter);
    }

    // Check right
    if (col < 5) {
        let foundLetter = letters.find(l => l.index === index + 1);
        if (foundLetter) adjacentLetters.push(foundLetter);
    }

    // Check down-left
    if (row < 8 && col > 0) {
        let foundLetter = letters.find(l => l.index === index + 5);
        if (foundLetter) adjacentLetters.push(foundLetter);
    }

    // Check down
    if (row < 8) {
        let foundLetter = letters.find(l => l.index === index + 6);
        if (foundLetter) adjacentLetters.push(foundLetter);
    }

    // Check down-right
    if (row < 8 && col < 5) {
        let foundLetter = letters.find(l => l.index === index + 7);
        if (foundLetter) adjacentLetters.push(foundLetter);
    }

    return adjacentLetters;
}
