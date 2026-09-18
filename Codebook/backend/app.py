from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)


DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "climate_visu",
    "user":"postgres",
    "password":"postgres",
}


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)



@app.route("/api/health", methods=["GET"])
def health():
    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
            "status": "ok",
            "database": "connected"
        })

    except Exception as error:
        print("Database connection error:", error)

        return jsonify({
            "status": "error",
            "database": "unavailable",
            "error": str(error)
        }), 500


@app.route("/api/codings", methods=["GET"])
def get_codings():
    coder_name = request.args.get("coder_name")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if coder_name:
            cursor.execute(
                """
                SELECT *FROM public.result WHERE coder_name = %s ORDER BY coded_at
                """,
                (coder_name,))
        else:
            cursor.execute(
                """
                SELECT * FROM public.result ORDER BY coded_at
                """)

        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        result = [dict(zip(column_names, row)) for row in rows]
        cursor.close()
        conn.close()

        return jsonify(result)

    except Exception as error:
        print("Error while loading codings:", error)
        return jsonify({"error": str(error)}), 500


# ============================================================
# SAVE / UPDATE CODING
# ============================================================

@app.route("/api/codings", methods=["POST"])
def save_coding():

    record = request.get_json()

    if not record:
        return jsonify({"error": "No record provided."}), 400

    record_id = record.get("record_id")
    coder_name = record.get("coder_name")

    if not record_id:
        return jsonify({"error": "record_id is required."}), 400

    if not coder_name:
        return jsonify({"error": "coder_name is required."}), 400


    columns = [
        "record_id",
        "coder_name",
        "source_organization",
        "source_figure_id",
        "source_figure_url",
        "media_outlet",
        "media_article_title",
        "media_article_url",
        "media_publication_date",
        "media_updated_date",
        "coding_confidence",
        "coder_notes",
        "source_image_filename",
        "source_image_export_path",
        "media_image_filename",
        "media_image_export_path",
        "media_csv_local_path",
        "media_csv_article_id",
        "media_csv_image_url",

        "data_variables_scope",
        "variables_data_added_count",
        "variables_data_removed_count",
        "variables_spatial_added_count",
        "variables_spatial_removed_count",
        "variables_temporal_added_count",
        "variables_temporal_removed_count",
        "spatial_scope",
        "spatial_scope_details",

        "temporal_scope",
        "temporal_scope_details",

        "data_aggregation_transformation",
        "data_aggregation_description",

        "uncertainty_visibility",
        "uncertainty_changed_type",
        "uncertainty_elements",
        "uncertainty_elements_other",

        "source_attribution_visibility",
        "source_attribution_type",

        "chart_type_relation",
        "chart_type_from",
        "chart_type_to",
        "chart_type_change_notes",

        "panel_count",
        "panel_count_source",
        "panel_count_media",

        "visual_density_change",
        "layout_reordering",

        "axes_scales",
        "axes_scales_description",

        "legend",
        "legend_description",

        "visual_emphasis",
        "visual_emphasis_description",

        "color_function",

        "visual_mapping",
        "visual_mapping_description",

        "annotations",
        "annotations_description",

        "external_notes_explanations",
        "external_notes_explanations_description",

        "decorations",

        "color_palette",
        "color_palette_description",

        "title_word_count_change",
        "subtitle_word_count_change",

        "media_title_function",
        "scientific_title_function",
        "media_subtitle_function",
        "scientific_subtitle_function",

        "message_fidelity",
        "message_fidelity_description",

        "narrative_frame",
        "narrative_frame_other",

        "coded_at",
    ]
    values = [record.get(column, "") for column in columns]


    column_sql = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    update_columns = [column for column in columns if column not in ("record_id", "coder_name")]

    update_sql = ", ".join(f"{column} = EXCLUDED.{column}" for column in update_columns)

    sql = f"""
        INSERT INTO public.result ({column_sql})
        VALUES ({placeholders})
        ON CONFLICT (record_id, coder_name)
        DO UPDATE SET {update_sql}
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"success": True,"record_id": record_id,"coder_name": coder_name})

    except Exception as error:
        print("Error while saving coding:", error)

        return jsonify({"success": False,"error": str(error)}), 500


# ============================================================
# STATUS
# ============================================================

@app.route("/api/status", methods=["GET"])
def get_status():

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                row_key,
                disposition,
                source_unclear,
                completed_by,
                completed_at,
                record_id,
                updated_by,
                updated_at
            FROM public.status
            ORDER BY row_key
            """
        )

        rows = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        result = [dict(zip(column_names, row)) for row in rows]

        cursor.close()
        conn.close()

        return jsonify(result)

    except Exception as error:
        print("Error while loading status:", error)

        return jsonify({"error": str(error)}), 500


# ============================================================
# SAVE / UPDATE STATUS
# ============================================================

@app.route("/api/status", methods=["POST"])
def save_status():

    status = request.get_json()

    if not status:
        return jsonify({"error": "No status provided."}), 400

    row_key = status.get("row_key")

    if not row_key:
        return jsonify({"error": "row_key is required."}), 400

    sql = """
        INSERT INTO public.status (
            row_key,
            disposition,
            source_unclear,
            completed_by,
            completed_at,
            record_id,
            updated_by,
            updated_at
        )
        VALUES (%s, %s, %s, %s,%s, %s, %s, %s)
        ON CONFLICT (row_key)
        DO UPDATE SET
            disposition = EXCLUDED.disposition,
            source_unclear = EXCLUDED.source_unclear,
            completed_by = EXCLUDED.completed_by,
            completed_at = EXCLUDED.completed_at,
            record_id = EXCLUDED.record_id,
            updated_by = EXCLUDED.updated_by,
            updated_at = EXCLUDED.updated_at
    """

    values = (
        row_key,
        status.get("disposition", ""),
        status.get("source_unclear", ""),
        status.get("completed_by", ""),
        status.get("completed_at", ""),
        status.get("record_id", ""),
        status.get("updated_by", ""),
        status.get("updated_at", ""),
    )

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(sql, values)

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"success": True,"row_key": row_key})

    except Exception as error:
        print("Error while saving status:", error)

        return jsonify({"success": False,"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)