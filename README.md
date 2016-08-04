# TIPS

master 里不要改POSCAR和POTCAR

材料分支 只改POSCAR和POTCAR 然后merge master

开发分支 不改POSCAR POTCAR

master merge 开发分支

test 分支在开发分支基础上 checkout 材料分支的 POSCAR和 POTCAR

---

# TODO

## DFT-PHY

！vasp的编译优化?比如Gamma Point Only（找老师/师兄吧，累死了）

## OA-DFT

！不完全计算vasp

！充分利用VASP的输出，包括弛豫(调研vasp)

！不浪费其他地方的WAVECAR，以及微扰

## ML-PSO

ML与PSO联合优化,ML指导PSO的方向

PSO的原理?phig,phip？两次ML(g,p)替代两个方向(g,p)？

！需要一个input sampled point, output minimum的ML

## BO

！spearmint

！随机过程/高斯过程

！调研BO的优势
