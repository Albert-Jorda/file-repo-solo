table_row_folder = document.querySelectorAll('tr.folder');
td_file = document.querySelectorAll(".file_open");
drpDwn_categ = document.querySelector('#categories');
drpDwn_orderBy = document.querySelector('#order_by');
drpDwn_sequence = document.querySelector('#sequence');

table_row_folder.forEach(trf => {
    trf.addEventListener("click", () => {
        let url = trf.getAttribute("data-url");
        document.location.href = url;
    });
});

td_file.forEach(tdf => {
    tdf.addEventListener("click", () => {
        let url = tdf.getAttribute("data-url");
        window.open(url, "_blank").focus();
    });
});


drpDwn_categ.addEventListener("change", () => {
    url = drpDwn_categ.options[drpDwn_categ.selectedIndex].getAttribute('data-url');
    document.location.href = url;
});

drpDwn_orderBy.addEventListener("change", () => {
    url = drpDwn_orderBy.options[drpDwn_orderBy.selectedIndex].getAttribute('data-url');
    document.location.href = url;
});

drpDwn_sequence.addEventListener("change", () => {
    url = drpDwn_sequence.options[drpDwn_sequence.selectedIndex].getAttribute('data-url');
    document.location.href = url;
});