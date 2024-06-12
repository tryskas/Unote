$(document).ready(function() {
    const table = document.getElementById('timetable');

    const rows = table.rows;
    const cellMap = {};

    // Traverse through all cells and group by their id
    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].cells;
        for (let j = 1; j < cells.length; j++) { // start from 1 to skip the time column
            const cell = cells[j];
            if (cell.id) {
                if (!cellMap[cell.id]) {
                    cellMap[cell.id] = [];
                }
                cellMap[cell.id].push(cell);
            }
        }
    }

    // Merge cells with the same id
    for (let id in cellMap) {
        const cells = cellMap[id];
        if (cells.length > 1) {
            const firstCell = cells[0];
            const rowspan = cells.length;

            firstCell.rowSpan = rowspan;
            for (let i = 1; i < cells.length; i++) {
                cells[i].remove();
            }
        }
    }
});