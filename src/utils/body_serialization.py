from typing import Dict

from pymunk import Body


def kinematic_body_to_dict(body: Body) -> Dict:
    return {
        "position": body.position,
        "velocity": body.velocity,
        "angle": body.angle,
        "angular_velocity": body.angular_velocity,
    }


def apply_params_to_kinematic_body_from_dict(body: Body, data: Dict):
    body.position = data["position"]
    body.velocity = data["velocity"]
    body.angle = data["angle"]
    body.angular_velocity = data["angular_velocity"]


def dynamic_body_to_dict(body: Body) -> Dict:
    return {
        "position": body.position,
        "mass": body.mass,
        "moment": body.moment,
        "velocity": body.velocity,
        "angle": body.angle,
        "angular_velocity": body.angular_velocity,
    }


def apply_params_to_dynamic_body_from_dict(body: Body, data: Dict):
    body.position = data["position"]
    body.velocity = data["velocity"]
    body.angle = data["angle"]
    body.angular_velocity = data["angular_velocity"]
