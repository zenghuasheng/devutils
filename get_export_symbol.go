package main

import (
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"log"
	"os"
	"path/filepath"
)

func main() {
	exportSymbol()
}

func exportSymbol() {
	// 获取命令行参数
	args := os.Args[1:]

	// 检查参数是否提供
	if len(args) == 0 {
		fmt.Println("请输入代码路径")
		return
	}

	// 获取要分析的文件的绝对路径
	fileName := args[0]
	var option string
	if len(args) > 1 {
		option = args[1]
	}
	// 获取文件所在目录的绝对路径
	pkgPath, err := filepath.Abs(filepath.Dir(fileName))
	if err != nil {
		log.Fatal(err)
	}
	// 解析包的源码
	fset := token.NewFileSet()
	pkgs, err := parser.ParseDir(fset, pkgPath, nil, parser.AllErrors)
	if err != nil {
		log.Fatal(err)
	}

	// 遍历解析得到的包
	for _, pkg := range pkgs {
		// 遍历包内文件
		for filePath, file := range pkg.Files {
			if option == "" && filePath != fileName {
				continue
			}
			// 遍历文件中的声明
			for _, decl := range file.Decls {
				switch d := decl.(type) {
				case *ast.GenDecl:
					// 判断是否是导出的标识符
					if d.Tok == token.VAR || d.Tok == token.CONST {
						// 遍历导出的标识符列表
						for _, spec := range d.Specs {
							switch s := spec.(type) {
							case *ast.ValueSpec:
								// 输出导出的变量和常量名
								for _, name := range s.Names {
									if !name.IsExported() {
										continue
									}
									fmt.Printf("%s %v\n", name.Name, name.Obj.Kind)
								}
							}
						}
					} else if d.Tok == token.TYPE {
						// 输出导出的结构体名
						for _, spec := range d.Specs {
							switch s := spec.(type) {
							case *ast.TypeSpec:
								if !s.Name.IsExported() {
									continue
								}
								fmt.Printf("%s struct\n", s.Name.Name)
							}
						}
					}
				case *ast.FuncDecl:
					// 输出导出的函数名
					if d.Name.IsExported() && !isMethod(d) {
						fmt.Printf("%s function\n", d.Name.Name)
					}
				}
			}
		}
	}
}

func isMethod(decl *ast.FuncDecl) bool {
	return decl.Recv != nil
}
