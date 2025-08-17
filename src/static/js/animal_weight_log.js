/*global $, _, asm, common, config, controller, dlgfx, edit_header, format, header, html, tableform, validate */

$(function() {

    "use strict";
    
    // Weight Log Module Version
    const WEIGHT_LOG_VERSION = "1.6.0";

    const animal_weight_log = {

        model: function() {
            const dialog = {
                add_title: _("Add weight entry"),
                edit_title: _("Edit weight entry"),
                edit_perm: 'va',
                close_on_ok: false,
                columns: 1,
                width: 550,
                fields: [
                    { json_field: "WEIGHT_DATE", post_field: "weightdate", label: _("Date"), type: "date", validation: "notblank", defaultval: new Date() },
                    { json_field: "WEIGHT", post_field: "weight", label: _("Weight"), type: "number", validation: "notblank" },
                    { post_field: "weightunit", label: _("Unit"), type: "select", 
                        options: "kg|" + _("kg") + "||lb|" + _("lb"),
                        defaultval: config.str("ShowWeightInLbs") == "Yes" ? "lb" : "kg"
                    },
                    { json_field: "USERNAME", post_field: "username", label: _("Recorded by"), type: "text", readonly: true }
                ]
            };

            const table = {
                rows: controller.rows,
                idcolumn: "ID",
                multiselect: true,
                edit: async function(row) {
                    await tableform.dialog_show_edit(dialog, row, {
                        onload: function() {
                            // Set weight unit based on display preference and convert if needed
                            let weightunit = config.str("ShowWeightInLbs") == "Yes" ? "lb" : "kg";
                            let weight = row.WEIGHT;
                            if (weightunit == "lb" && weight) {
                                weight = (weight * 2.20462).toFixed(1);
                            }
                            $("#weight").val(weight);
                            $("#weightunit").val(weightunit);
                        }
                    });
                    tableform.fields_update_row(dialog.fields, row);
                    await tableform.fields_post(dialog.fields, "mode=update&weightid=" + row.ID, "animal_weight_log");
                    tableform.table_update(table);
                    tableform.dialog_close();
                },
                columns: [
                    { field: "WEIGHT_DATE", display: _("Date"), initialsort: true, initialsortdirection: "desc", formatter: tableform.format_date },
                    { field: "WEIGHT", display: _("Weight"), formatter: function(row) {
                        if (config.str("ShowWeightInLbs") == "Yes") {
                            return (row.WEIGHT * 2.20462).toFixed(3) + " lb";
                        } else {
                            return row.WEIGHT.toFixed(3) + " kg";
                        }
                    }},
                    { field: "USERNAME", display: _("Recorded by") },
                    { field: "CREATED_DATE", display: _("Created"), formatter: tableform.format_datetime }
                ]
            };

            const buttons = [
                { id: "new", text: _("New Weight Entry"), icon: "new", enabled: "always", perm: "va",
                    click: async function() { 
                        await tableform.dialog_show_add(dialog, {
                            onload: function() {
                                $("#username").val(asm.user);
                                let weightunit = config.str("ShowWeightInLbs") == "Yes" ? "lb" : "kg";
                                $("#weightunit").val(weightunit);
                            }
                        });
                        let response = await tableform.fields_post(dialog.fields, "mode=create&animalid=" + controller.animal.ID, "animal_weight_log");
                        let row = {};
                        row.ID = response;
                        tableform.fields_update_row(dialog.fields, row);
                        row.USERNAME = asm.user;
                        row.CREATED_DATE = new Date();
                        controller.rows.push(row);
                        tableform.table_update(table);
                        tableform.dialog_close();
                    } 
                },
                { id: "delete", text: _("Delete"), icon: "delete", enabled: "multi", perm: "va",
                    click: async function() { 
                        await tableform.delete_dialog();
                        tableform.buttons_default_state(buttons);
                        let ids = tableform.table_ids(table);
                        await common.ajax_post("animal_weight_log", "mode=delete&ids=" + ids);
                        tableform.table_remove_selected_from_json(table, controller.rows);
                        tableform.table_update(table);
                    } 
                }
            ];

            this.dialog = dialog;
            this.table = table;
            this.buttons = buttons;
        },

        render: function() {
            try {
                console.log(`[WEIGHT_LOG] Version ${WEIGHT_LOG_VERSION} - Rendering weight log for animal ${controller.animal.ID}`);
                console.log(`[WEIGHT_LOG] Available data:`, controller.rows ? controller.rows.length + " rows" : "No rows data");
                
                this.model();
                let s = "";
                s += tableform.dialog_render(this.dialog);
                s += edit_header.animal_edit_header(controller.animal, "weight_log", controller.tabcounts);
                s += tableform.buttons_render(this.buttons);
                s += tableform.table_render(this.table);
                s += html.content_footer();
                
                console.log(`[WEIGHT_LOG] Version ${WEIGHT_LOG_VERSION} - Render completed successfully, HTML length: ${s.length}`);
                return s;
            } catch (err) {
                console.error(`[WEIGHT_LOG] Version ${WEIGHT_LOG_VERSION} - Error rendering weight log:`, err);
                return "<p>Error loading weight log</p>";
            }
        },

        bind: function() {
            try {
                console.log(`[WEIGHT_LOG] Version ${WEIGHT_LOG_VERSION} - Binding weight log events`);
                $(".asm-tabbar").asmtabs();
                tableform.dialog_bind(this.dialog);
                tableform.buttons_bind(this.buttons);
                tableform.table_bind(this.table, this.buttons);
                console.log(`[WEIGHT_LOG] Version ${WEIGHT_LOG_VERSION} - Bind completed successfully`);
            } catch (err) {
                console.error(`[WEIGHT_LOG] Version ${WEIGHT_LOG_VERSION} - Error binding weight log:`, err);
            }
        },

        sync: function() {
            try {
                // Reload data if needed  
                if (controller && controller.rows) {
                    tableform.table_update(this.table);
                }
            } catch (err) {
                console.error("Error syncing weight log:", err);
            }
        },

        destroy: function() {
            try {
                tableform.dialog_destroy();
            } catch (err) {
                console.error("Error destroying weight log:", err);
            }
        },

        name: "animal_weight_log",
        animation: "book",
        autofocus: "#asm-content button:first",
        title:  function() { return common.substitute(_("{0} - {1} ({2} {3} aged {4})"), { 
            0: controller.animal.ANIMALNAME, 1: controller.animal.CODE, 2: controller.animal.SEXNAME,
            3: controller.animal.SPECIESNAME, 4: controller.animal.ANIMALAGE }); },
        routes: {
            "animal_weight_log": function() { 
                console.log(`[WEIGHT_LOG] Version ${WEIGHT_LOG_VERSION} - Loading weight log module for animal ID: ${this.qs.id}`);
                common.module_loadandstart("animal_weight_log", "animal_weight_log?id=" + this.qs.id);
            }
        }

    };

    common.module_register(animal_weight_log);
    
    // Log module registration with version
    console.log(`[WEIGHT_LOG] Version ${WEIGHT_LOG_VERSION} - Module registered successfully`);

});