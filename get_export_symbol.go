package main

import (
	"encoding/json"
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"log"
	"os"
	"path/filepath"
)

func main() {
	/**
	新的情况，别的文件还可能引用这个包的没导出的常量
	此文件：所有 symbol
	包：
	symbol: 导出的、未导出的
	要检查 4 种情况：
	1. 此文件用了包的导出的常量
	2. 此文件用了包的未导出的常量
	3. 包的其他文件用了此文件的导出的常量
	4. 包的其他文件用了此文件的未导出的常量

	*/
	exportSymbol()
}

type Symbol struct {
	Name string `json:"name"`
	Kind string `json:"kind"`
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
	symbols := make(map[string][]Symbol)
	symbols["exported"] = make([]Symbol, 0)
	symbols["unexported"] = make([]Symbol, 0)
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
									if name.Name == "_" {
										continue
									}
									if name.IsExported() {
										symbols["exported"] = append(symbols["exported"],
											Symbol{Name: name.Name, Kind: d.Tok.String()})
									} else {
										symbols["unexported"] = append(symbols["unexported"],
											Symbol{Name: name.Name, Kind: d.Tok.String()})
									}
								}
							}
						}
					} else if d.Tok == token.TYPE {
						// 输出导出的结构体名
						for _, spec := range d.Specs {
							switch s := spec.(type) {
							case *ast.TypeSpec:
								if s.Name.IsExported() {
									symbols["exported"] = append(symbols["exported"],
										Symbol{Name: s.Name.Name, Kind: d.Tok.String()})
								} else {
									symbols["unexported"] = append(symbols["unexported"],
										Symbol{Name: s.Name.Name, Kind: d.Tok.String()})
								}
							}
						}
					}
				case *ast.FuncDecl:
					if isMethod(d) {
						// 如果是方法，跳过
						continue
					}
					if d.Name.IsExported() {
						symbols["exported"] = append(symbols["exported"],
							Symbol{Name: d.Name.Name, Kind: "func"})
					} else {
						symbols["unexported"] = append(symbols["unexported"],
							Symbol{Name: d.Name.Name, Kind: "func"})
					}
				}
			}
		}
	}
	// 转为 json 输出
	bytes, err := json.Marshal(symbols)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(bytes))
}

func isMethod(decl *ast.FuncDecl) bool {
	return decl.Recv != nil
}
