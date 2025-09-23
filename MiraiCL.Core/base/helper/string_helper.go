package helper

import "strings"

func IsEmpty(str string) (ret bool) {
	return str == ""
}

func IsBlank(str string) (ret bool) {
	return strings.TrimSpace(str) == ""
}

func EqualIgnoreCase(str string,str2 string){
	
}

