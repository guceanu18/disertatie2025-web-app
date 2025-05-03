from flask import Blueprint, render_template, request, redirect, url_for, flash
from disertatie2025_api_client import RouterClient

main = Blueprint("main", __name__)

api = RouterClient(base_url="http://127.0.0.1:8000")

@main.route("/")
def list_routers():
    routers = api.list_routers()
    return render_template("list_routers.html", routers=routers)

@main.route("/show", methods=["POST"])
def run_show_command():
    router_name = request.form["router_name"]
    command = request.form["command"]
    result = api.run_show_command(router_name, command)
    return render_template("show_result.html", router_name=router_name, command=command, result=result)

@main.route("/push", methods=["POST"])
def push_config():
    router_name = request.form["router_name"]
    config = request.form["config"]
    result = api.push_config(router_name, config)
    return render_template("push_result.html", router_name=router_name, result=result)
