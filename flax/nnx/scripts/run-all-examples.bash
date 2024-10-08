set -e

source .venv/bin/activate
cd flax/nnx

for f in $(find examples/toy_examples -name "*.py" -maxdepth 1); do
    echo -e "\n---------------------------------"
    echo "$f"
    echo "---------------------------------"
    MPLBACKEND=Agg python "$f"
done
