if [ -f $1.hrc ]
then
  python ../../hrc-minizinc/hrc-to-minizinc.py 0 --no-presolve < $1.hrc > $1.dzn && \
  minizinc ../../hrc-minizinc/hrc.mzn $1.dzn
else
  echo "Usage: $0 INSTANCE    (omit .hrc extension)"
fi
