from flask import Flask, request, redirect, render_template
from odf.opendocument import load, OpenDocumentSpreadsheet
from odf.table import TableRow, TableCell
from odf.text import P
import os

app = Flask(__name__)
ODS_PATH = "comm.ods"
commentaires = []

def charger_commentaires():
    if not os.path.exists(ODS_PATH):
        return

    doc = load(ODS_PATH)
    rows = doc.spreadsheet.getElementsByType(TableRow)

    for row in rows:
        cells = row.getElementsByType(TableCell)
        if len(cells) >= 2:
            pseudo_parts = cells[0].getElementsByType(P)
            commentaire_parts = cells[1].getElementsByType(P)

            pseudo = ""
            if pseudo_parts and pseudo_parts[0].firstChild:
                pseudo = pseudo_parts[0].firstChild.data

            commentaire = ""
            if commentaire_parts and commentaire_parts[0].firstChild:
                commentaire = commentaire_parts[0].firstChild.data

            if pseudo and commentaire:
                commentaires.append((pseudo, commentaire))


def enregistrer_ods():
    doc = OpenDocumentSpreadsheet()
    from odf.table import Table
    table = Table(name="Commentaires")
    doc.spreadsheet.addElement(table)

    for pseudo, commentaire in commentaires:
        row = TableRow()
        for value in [pseudo, commentaire]:
            cell = TableCell()
            cell.addElement(P(text=value))
            row.addElement(cell)
        table.addElement(row)

    doc.save(ODS_PATH)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", commentaires=commentaires)

@app.route("/comment", methods=["POST"])
def comment():
    pseudo = request.form["pseudo"]
    commentaire = request.form["commentaire"]
    commentaires.append((pseudo, commentaire))
    enregistrer_ods()
    return redirect("/")

# 👇 Place ce bloc tout à la fin
if __name__ == "__main__":
    charger_commentaires()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
