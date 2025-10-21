import os
import shutil

# Base folder containing the 4 original input cards
base_dir = "InputCards"
base_name = "Zh_M125_ToAA_20_Tobbgg"

# Mass points (in GeV)
mass_points = [12, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]

# Loop over each mass point
for mA in mass_points:
    folder_name = f"Inputcards_M{mA}"
    os.makedirs(folder_name, exist_ok=True)

    for fname in os.listdir(base_dir):
        src = os.path.join(base_dir, fname)
        if not os.path.isfile(src):
            continue

        # Replace "15GeV" in file names with the actual mass point
        new_fname = fname.replace("20", f"{mA}")
        dst = os.path.join(folder_name, new_fname)
        shutil.copy(src, dst)

        # Modify customizecards.dat
        if "customizecards" in fname:
            mzdinput = 2 * mA
            whs = 5.237950e-03  # constant unless otherwise needed
            with open(dst, "w") as f:
                f.write(f"""set param_card mzdinput {mzdinput:.6e}
set param_card mhsinput {mA:.6e}
set param_card epsilon 1.000000e-10
set param_card kap 5.000000e-01
set param_card whs {whs:.6e}
set param_card mass 35 {mA:.6e}
set param_card mass 1023 {mzdinput:.6e}
""")

        # Modify proc_card.dat
        elif "proc_card" in fname:
            with open(src, "r") as f:
                content = f.read()
            # Replace output line
            new_output_line = f"output Zh_M125_ToAA_{mA}_Tobbgg"
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if line.strip().startswith("output Zh_M125_ToAA_"):
                    lines[i] = new_output_line
                    break
            with open(dst, "w") as f:
                f.write("\n".join(lines) + "\n")

print("Generated inputcard folders:")
for mA in mass_points:
    print(f"  - Inputcards_M{mA}/")

