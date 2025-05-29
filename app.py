from flask import Flask, render_template, request, redirect, url_for, flash
import os
from analysis_processor import process_file

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "data/"
app.config["OUTPUT_FOLDER"] = "static/"
app.secret_key = os.urandom(24)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    if "file" not in request.files or request.files["file"].filename == "":
        flash("No file selected!", "error")
        return redirect(url_for("index"))

    file = request.files["file"]
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    try:
        (
            numeric_columns,
            pca_df,
            summary_html,
            pca_plot_path,
            heatmap_path,
            processed_file_path,
        ) = process_file(file_path, app.config["OUTPUT_FOLDER"])
    except Exception as e:
        flash(f"Error processing file: {e}", "error")
        return redirect(url_for("index"))

    flash("File processed successfully!", "success")
    return render_template(
        "results.html",
        numeric_columns=numeric_columns,
        pca_table=pca_df.to_html(classes="table table-striped", index=False),
        summary_table=summary_html,
        plot_url=pca_plot_path,
        heatmap_url=heatmap_path,
        processed_file_url=processed_file_path,
    )


if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)
    app.run(debug=True)
