from user import (
    Register,
    Login,
    QueryUser,
    ChangeRole,
    UpdateAvatar,
    ChangeGamemod,
    UpdateNickname,
    RestPwd,
    GetUsers,
)
import json
from untils import create_token, validate_token, hash256
from flask import Flask, request

app = Flask(__name__)


# Register
@app.route("/register", methods=["POST"])
def register():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if len(json_data) == 3:
        pass
    else:
        return json.dumps({"sucess": False, "message": "Lack of args!"})
    if QueryUser(json_data["account"]) is not None:
        return json.dumps({"sucess": False, "message": "Account Already Exits!"})
    try:
        Register(json_data["account"], json_data["pwd"], json_data["nickname"])
    except:
        return json.dumps({"sucess": False, "message": "Database Error!"})
    return json.dumps({"sucess": True, "message": "Register Successfully!"})


# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if len(json_data) == 2:
        pass
    else:
        return json.dumps({"sucess": False, "message": "Lack of args!"})
    try:
        user_detail = Login(json_data["account"], json_data["pwd"])
        if user_detail:
            token = create_token(user_detail)
            return json.dumps({"sucess": False, "token": token})
        else:
            return json.dumps({"sucess": False, "message": "Login Detail Error!"})
    except:
        return json.dumps({"sucess": False, "message": "Database Error!"})


# User Infomatiom (Request by user himself)
@app.route("/userinfo", methods=["GET"])
def userinfo():
    auth_token = (request.headers.get("Authorization")).replace("Bearer ", "")
    payload_data, message = validate_token(auth_token)
    if message is not None:
        return json.dumps({"sucess": False, "message": message})
    else:
        this_user = QueryUser(payload_data["account"])
        return json.dumps(
            {
                "sucess": True,
                "message": "Get User Informatiom Successully!",
                "data": {
                    "account": this_user.account,
                    "role": this_user.role,
                    "nickname": this_user.nickname,
                    "avatar": this_user.avatar,
                    "gamemode": this_user.gamemode,
                },
            }
        )


# Change Role
@app.route("/changerole", methods=["POST"])
def changerole():
    auth_token = (request.headers.get("Authorization")).replace("Bearer ", "")
    payload_data, message = validate_token(auth_token)
    if message is not None:
        return json.dumps({"sucess": False, "message": message})
    else:
        pass
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if payload_data["role"] == "admin":
        ChangeRole(json_data["account"], json_data["role"])
        return json.dumps(
            {
                "sucess": True,
                "message": "Role of %s has changed Successfully!"
                % json_data["account"],
            }
        )
    else:
        return json.dumps({"sucess": False, "message": "Access Denied!"})


# Change Gamemode
@app.route("/changmode", methods=["POST"])
def changmode():
    auth_token = (request.headers.get("Authorization")).replace("Bearer ", "")
    payload_data, message = validate_token(auth_token)
    if message is not None:
        return json.dumps({"sucess": False, "message": message})
    else:
        pass
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if payload_data["role"] == "admin":
        ChangeGamemod(json_data["account"], json_data["gamemode"])
        return json.dumps(
            {
                "sucess": True,
                "message": "Gamemode of %s has changed Successfully!"
                % json_data["account"],
            }
        )
    else:
        return json.dumps({"sucess": False, "message": "Access Denied!"})


# Update Avatar
@app.route("/updateavatar", methods=["POST"])
def updateavatar():
    auth_token = (request.headers.get("Authorization")).replace("Bearer ", "")
    payload_data, message = validate_token(auth_token)
    if message is not None:
        return json.dumps({"sucess": False, "message": message})
    else:
        pass
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if payload_data["account"] == json_data["account"]:
        UpdateAvatar(json_data["account"], json_data["avatar"])
        this_user = QueryUser(payload_data["account"])
        return json.dumps(
            {
                "sucess": True,
                "message": "Avatar of %s has changed Successfully!"
                % json_data["account"],
                "new_token": create_token(
                    {
                        "account": this_user.account,
                        "role": this_user.role,
                        "nickname": this_user.nickname,
                        "avatar": this_user.avatar,
                        "gamemode": this_user.gamemode,
                    }
                ),
            }
        )
    else:
        return json.dumps({"sucess": False, "message": "Access Denied!"})


# Update Nickname
@app.route("/updatenickname", methods=["POST"])
def updatenickname():
    auth_token = (request.headers.get("Authorization")).replace("Bearer ", "")
    payload_data, message = validate_token(auth_token)
    if message is not None:
        return json.dumps({"sucess": False, "message": message})
    else:
        pass
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if payload_data["account"] == json_data["account"]:
        UpdateNickname(json_data["account"], json_data["nickname"])
        this_user = QueryUser(payload_data["account"])
        return json.dumps(
            {
                "sucess": True,
                "message": "Nickname of %s has changed Successfully!"
                % json_data["account"],
                "new_token": create_token(
                    {
                        "account": this_user.account,
                        "role": this_user.role,
                        "nickname": this_user.nickname,
                        "avatar": this_user.avatar,
                        "gamemode": this_user.gamemode,
                    }
                ),
            }
        )
    else:
        return json.dumps({"sucess": False, "message": "Access Denied!"})


# Rest Password
@app.route("/restpwd", methods=["POST"])
def restpwd():
    auth_token = (request.headers.get("Authorization")).replace("Bearer ", "")
    payload_data, message = validate_token(auth_token)
    if message is not None:
        return json.dumps({"sucess": False, "message": message})
    else:
        pass
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if payload_data["account"] == json_data["account"]:
        this_user = QueryUser(payload_data["account"])
        print(this_user.pwd)
        if this_user.pwd == hash256(json_data["original_pwd"]):
            RestPwd(json_data["account"], json_data["changed_pwd"])
            this_user = QueryUser(payload_data["account"])
            return json.dumps(
                {
                    "sucess": True,
                    "message": "Password of %s has changed Successfully!"
                    % json_data["account"],
                    "new_token": create_token(
                        {
                            "account": this_user.account,
                            "role": this_user.role,
                            "nickname": this_user.nickname,
                            "avatar": this_user.avatar,
                            "gamemode": this_user.gamemode,
                        }
                    ),
                }
            )
        else:
            return json.dumps(
                {"sucess": False, "message": "Original Password Not Match!"}
            )
    else:
        return json.dumps({"sucess": False, "message": "Access Denied!"})


# Get User Info by account
@app.route("/getuser", methods=["GET"])
def getuser():
    auth_token = (request.headers.get("Authorization")).replace("Bearer ", "")
    payload_data, message = validate_token(auth_token)
    if message is not None:
        return json.dumps({"sucess": False, "message": message})
    else:
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        this_user = QueryUser(json_data["account"])
        return json.dumps(
            {
                "sucess": True,
                "message": "Get User Informatiom Successully!",
                "data": {
                    "account": this_user.account,
                    "role": this_user.role,
                    "nickname": this_user.nickname,
                    "avatar": this_user.avatar,
                    "gamemode": this_user.gamemode,
                },
            }
        )


# Get All Users
@app.route("/getalluser", methods=["GET"])
def getalluser():
    auth_token = (request.headers.get("Authorization")).replace("Bearer ", "")
    payload_data, message = validate_token(auth_token)
    if message is not None:
        return json.dumps({"sucess": False, "message": message})
    else:
        pass
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if payload_data["role"] == "admin":
        users = GetUsers(json_data["page"], json_data["pagesize"])
        return json.dumps({"sucess": True, "message": "Successfully!", "data": users})
    else:
        return json.dumps({"sucess": False, "message": "Access Denied!"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")

