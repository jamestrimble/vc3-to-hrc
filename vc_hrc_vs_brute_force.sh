if [ -f $1.graph ]
then
  MINVC=$(python min_vc.py $1.graph)
  echo Size of min vertex cover for $1.graph: $MINVC
  python vc3-to-hrc.py $1.graph $MINVC > tmp/tmp.hrc
  ./minizinc_solve.sh tmp/tmp
  if [ $? -ne 0 ]; then echo "$1 satisfiable instance failed"; fi
  if [ $MINVC -gt 0 ]; then
    python vc3-to-hrc.py $1.graph $(($MINVC-1)) > tmp/tmp.hrc
    ./minizinc_solve.sh tmp/tmp > /dev/null
    if [ $? -ne 1 ]; then echo "$1 unsatisfiable instance failed"; fi
  fi
else
  echo "Usage: $0 INSTANCE    (omit .hrc extension)"
fi
