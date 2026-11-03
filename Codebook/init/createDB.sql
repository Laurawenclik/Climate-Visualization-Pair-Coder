CREATE TABLE IF NOT EXISTS public.result
(
    record_id text,
    coder_name text,
    source_organization text,
    source_figure_id text,
    source_figure_url text,
    media_outlet text,
    media_article_title text,
    media_article_url text,
    media_publication_date text,
    media_updated_date text,
    coding_confidence text,
    coder_notes text,
    source_image_filename text,
    source_image_export_path text,
    media_image_filename text,
    media_image_export_path text,
    media_csv_local_path text,
    media_csv_article_id text,
    media_csv_image_url text,

    data_variables_scope text,
    variables_data_added_count text,
    variables_data_removed_count text,
    variables_spatial_added_count text,
    variables_spatial_removed_count text,
    variables_temporal_added_count text,
    variables_temporal_removed_count text,

    uncertainty_visibility text,
    uncertainty_changed_type text,
    source_attribution_visibility text,
    source_attribution_type text,

    chart_type_relation text,
    chart_type_from text,
    chart_type_to text,
    visual_density_change text,
    layout_reordering text,

    legend text,
    legend_description text,
    visual_emphasis text,
    visual_emphasis_description text,

    color_function text,
    visual_mapping text,
    visual_mapping_description text,

    annotations text,
    annotations_description text,

    external_notes_explanations text,
    external_notes_explanations_description text,

    decorations text,

    color_palette text,
    color_palette_description text,

    title_word_count_change text,
    subtitle_word_count_change text,

    media_title_function text,
    scientific_title_function text,
    media_subtitle_function text,
    scientific_subtitle_function text,

    narrative_frame text,
    coded_at text,

    spatial_scope_details text,
    temporal_scope_details text,
    data_aggregation_transformation text,
    data_aggregation_description text,
    uncertainty_elements text,
    uncertainty_elements_other text,
    chart_type_change_notes text,
    panel_count text,
    panel_count_source text,
    panel_count_media text,
    axes_scales text,
    axes_scales_description text,
    message_fidelity text,
    message_fidelity_description text,
    narrative_frame_other text,

    CONSTRAINT result_record_coder_unique
        UNIQUE (record_id, coder_name)
);


CREATE TABLE IF NOT EXISTS public.status
(
    row_key character varying,
    disposition character varying,
    source_unclear character varying,
    completed_by character varying,
    completed_at character varying,
    record_id character varying,
    updated_by character varying,
    updated_at character varying,

    CONSTRAINT status_row_key_unique
        UNIQUE (row_key)
);