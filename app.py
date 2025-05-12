from flask import Flask, render_template, request, redirect, url_for, flash
import os
from analysis_processor import process_file

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "data/"  # Folder for uploaded files
app.config["OUTPUT_FOLDER"] = "static/"  # Folder for processed plots and datasets
app.secret_key = os.urandom(24)  # Required for flashing messages

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    if "file" not in request.files:
        flash("No file uploaded!", "error")
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        flash("No file selected!", "error")
        return redirect(request.url)

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)  # Save uploaded file

    # Perform analysis
    try:
        numeric_columns, pca_df, plot_path, processed_file_path = process_file(
            file_path, app.config["OUTPUT_FOLDER"]
        )
    except Exception as e:
        flash(f"Error processing file: {e}", "error")
        return redirect(request.url)

    # Flash success message
    flash("File processed successfully!", "success")

    # Render results
    return render_template(
        "results.html",
        numeric_columns=numeric_columns,
        pca_table=pca_df.to_html(classes="table table-striped", index=False),
        plot_url=plot_path,
        processed_file_url=processed_file_path,
    )


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    if not os.path.exists(app.config["OUTPUT_FOLDER"]):
        os.makedirs(app.config["OUTPUT_FOLDER"])
    app.run(debug=True)
