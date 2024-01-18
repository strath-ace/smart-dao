Create folder for app

# Create basic template called adder
erdpy contract new app_name --template adder
# Open new template in VS code
code crowdfunding

# File to edit
First update Cargo.toml
src/main.rs


# Build contract
cd app_name
erdpy contract build

# Test contract
erdpy contract test
"*" in expect column means any value


Change all .toml files
Change src/empty.rs to better name (Not main.rs) 


