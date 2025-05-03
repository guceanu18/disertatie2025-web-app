from flask import Blueprint, render_template, request, redirect, url_for, flash
from disertatie2025_api_client import RouterClient

main = Blueprint("main", __name__)

api = RouterClient()

@main.route("/")
def list_routers():
    routers = api.list_routers()
    return render_template("list_routers.html", routers=routers)

@main.route("/add_router", methods=["GET", "POST"])
def add_router():
    if request.method == "POST":
        name = request.form.get("name")
        mgmt_ip = request.form.get("mgmt_ip")
        site = request.form.get("site")
        api.add_router(name=name, mgmt_ip=mgmt_ip, site=site)
        flash("Router added successfully!")
        return redirect(url_for("main.list_routers"))
    return render_template("add_router.html")

@main.route("/delete_routers", methods=["POST"])
def delete_routers():
    selected = request.form.getlist("selected_routers")
    for name in selected:
        api.delete_router(name)
    flash(f"Deleted {len(selected)} router(s).")
    return redirect(url_for("main.list_routers"))

@main.route("/update_router/<name>", methods=["GET", "POST"])
def update_router(name):
    if request.method == "POST":
        data = {
            "new_name": request.form.get("new_name"),
            "mgmt_ip": request.form.get("mgmt_ip"),
            "site": request.form.get("site")
        }
        api.update_router(name, **data)
        flash("Router updated successfully.")
        return redirect(url_for("main.list_routers"))
    # Pre-fill with current data
    router = next((r for r in api.list_routers() if r["name"] == name), None)
    return render_template("update_router.html", router=router)

@main.route("/run_command/<router_name>", methods=["GET", "POST"])
def run_command(router_name):
    output = None
    if request.method == "POST":
        command = request.form.get("command")
        try:
            output = api.run_command(router_name, command)
            flash("Command executed successfully.")
        except Exception as e:
            flash(f"Error: {str(e)}")
    return render_template("run_command.html", router_name=router_name, output=output)

@main.route("/push", methods=["POST"])
def push_config():
    router_name = request.form["router_name"]
    config = request.form["config"]
    result = api.push_config(router_name, config)
    return render_template("push_result.html", router_name=router_name, result=result)
