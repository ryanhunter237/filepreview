import svgwrite
import math


# Function to draw a gear with a center circle, filled area, and text inside the circle
def draw_gear_with_text_in_center(
    file_name=f"gear.svg",
    radius=50,
    teeth=12,
    tooth_depth=10,
    tooth_width=10,
    slant_angle=4,
    inner_circle_radius=30,
):
    # Create an SVG file
    dwg = svgwrite.Drawing(file_name, profile="tiny", size=("200px", "200px"))

    # Center of the gear
    center = (100, 100)

    # Angle between each tooth
    angle_step = 2 * math.pi / teeth
    half_tooth_angle = math.radians(tooth_width)
    slant_offset = math.radians(slant_angle)

    # Points for the gear
    points = []
    for i in range(teeth):
        # Angles for this tooth
        angle = i * angle_step
        angle_left = angle - half_tooth_angle + slant_offset
        angle_right = angle + half_tooth_angle - slant_offset
        angle_left_base = angle - half_tooth_angle
        angle_right_base = angle + half_tooth_angle

        # Outer points (tooth top)
        x_outer_left = center[0] + (radius + tooth_depth) * math.sin(angle_left)
        y_outer_left = center[1] - (radius + tooth_depth) * math.cos(angle_left)

        x_outer_right = center[0] + (radius + tooth_depth) * math.sin(angle_right)
        y_outer_right = center[1] - (radius + tooth_depth) * math.cos(angle_right)

        # Inner points (tooth base)
        x_inner_left = center[0] + radius * math.sin(angle_left_base)
        y_inner_left = center[1] - radius * math.cos(angle_left_base)

        x_inner_right = center[0] + radius * math.sin(angle_right_base)
        y_inner_right = center[1] - radius * math.cos(angle_right_base)

        # Add points for the tooth
        points.append((x_inner_left, y_inner_left))  # Inner left
        points.append((x_outer_left, y_outer_left))  # Outer left
        points.append((x_outer_right, y_outer_right))  # Outer right
        points.append((x_inner_right, y_inner_right))  # Inner right

    # Define the outer gear shape
    gear_path_data = "M " + " ".join(f"{x},{y}" for x, y in points) + " Z"

    # Define the inner circle
    inner_circle_path_data = (
        f"M {center[0] + inner_circle_radius},{center[1]} "
        + f"A {inner_circle_radius},{inner_circle_radius} 0 1,0 "
        + f"{center[0] - inner_circle_radius},{center[1]} "
        + f"A {inner_circle_radius},{inner_circle_radius} 0 1,0 "
        + f"{center[0] + inner_circle_radius},{center[1]} Z"
    )

    # Combine the outer gear and inner circle into a single path
    combined_path = dwg.path(
        d=gear_path_data + " " + inner_circle_path_data,
        fill="#C70C00",
        stroke="black",
        stroke_width=1,
        fill_rule="evenodd",  # Ensure the inner circle is "cut out"
    )
    dwg.add(combined_path)

    # Save the SVG file
    dwg.save()


# Generate the gear SVG file with text in the center
draw_gear_with_text_in_center()
