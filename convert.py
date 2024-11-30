def convert_to_csv(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Prepare the output list for CSV lines
    csv_data = ["x1,y1,z1,x2,y2,z2"]

    # Parse the text file
    for i in range(0, len(lines), 3):  # Each block is 3 lines long
        if "Position:" in lines[i + 1] and "End position:" in lines[i + 2]:
            # Extract coordinates
            position = lines[i + 1].split("Position:")[1].strip().strip("()")
            end_position = lines[i + 2].split("End position:")[1].strip().strip("()")

            # Format as CSV
            csv_line = f"{position}, {end_position}"
            csv_data.append(csv_line)

    # Write to the output file
    with open(output_file, 'w') as file:
        file.write("\n".join(csv_data))

    print(f"Data successfully converted to {output_file}")

# Input and output file paths
input_file = "test4.txt"  # Replace with your input text file name
output_file = "output4.csv"  # Replace with your desired output CSV file name

convert_to_csv(input_file, output_file)
