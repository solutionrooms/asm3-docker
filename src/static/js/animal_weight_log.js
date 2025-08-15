/*global $, _, asm, common, config, controller, dlgfx, edit_header, format, header, html, tableform, validate */

$(function() {

    "use strict";

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
                            return (row.WEIGHT * 2.20462).toFixed(1) + " lb";
                        } else {
                            return row.WEIGHT.toFixed(1) + " kg";
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

            return {
                dialog: dialog,
                table: table, 
                buttons: buttons
            };
        },

        render: function() {
            console.log("WEIGHT_LOG: render() called");
            console.log("WEIGHT_LOG: controller=", controller);
            let m = this.model();
            console.log("WEIGHT_LOG: model=", m);
            let s = html.content_header(controller.animal.CODE + " " + controller.animal.ANIMALNAME);
            s += tableform.dialog_render(m.dialog);
            s += edit_header.animal_edit_header(controller.animal, "weight_log", controller.tabcounts);
            s += tableform.buttons_render(m.buttons);
            s += tableform.table_render(m.table);
            s += html.content_footer();
            console.log("WEIGHT_LOG: rendered HTML length=", s.length);
            return s;
        },

        bind: function() {
            $(".asm-tabbar").asmtabs();
            tableform.dialog_bind(this.model().dialog);
            tableform.buttons_bind(this.model().buttons);
            tableform.table_bind(this.model().table);
        },

        sync: function() {
            // No special sync needed for weight log
        },

        destroy: function() {
            common.widget_destroy("#animal");
        },

        name: "animal_weight_log",
        animation: "book",
        autofocus: "#asm-content button:first",
        title:  function() { return common.substitute(_("{0} - {1} ({2} {3} aged {4})"), { 
            0: controller.animal.ANIMALNAME, 1: controller.animal.CODE, 2: controller.animal.SEXNAME,
            3: controller.animal.SPECIESNAME, 4: controller.animal.ANIMALAGE }); },
        routes: {
            "animal_weight_log": function() { 
                common.module_loadandstart("animal_weight_log", "animal_weight_log?id=" + this.qs.id);
            }
        }

    };

    common.module_register(animal_weight_log);

});