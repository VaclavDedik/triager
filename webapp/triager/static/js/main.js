function select(elem) {
    var sel = window.getSelection();
    var range = sel.getRangeAt(0);
    range.selectNode(elem);
    sel.addRange(range);
}