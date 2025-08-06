#

# HUMAN TESTS
## Higher ranking number = More negative
##  10 > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2 > 1

#### T1 MOCK INSTALLER--- 
# C:\Users\mauricmm\UiO Dropbox\Mauricio Mandujano Manriquez\CMLRdata\
# ├── data_in/          ✅ External data directory created
# │   ├── mock_data_01.csv      ✅ Data files detected
# │   └── revu_data_01.csv      ✅ Multiple datasets available
# └── data_out/         ✅ External export directory created
#     ├── mock/         ✅ Per-dataset organization
#     └── overall/      ✅ Overall project exports


#### T2

#
# Get-ChildItem -Path "src" -Recurse -Include "*.py" | Select-String -Pattern "^(import|from)" | Sort-Object | Get-Unique
