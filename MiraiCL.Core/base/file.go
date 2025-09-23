package base

import (
	"os"
	"io"
)

func ReadAsString(path string)(ret string,err error){
	file,err:= ReadAsStream(path)
	if (err != nil){
		return "",err
	}
	defer file.Close()
	content,err := io.ReadAll(file)
	if (err != nil){
		return "",err
	}
	return string(content),nil
}

func ReadAsByte(path string)(ret []byte,err error){
	file,err:= ReadAsStream(path)
	if (err != nil){
		return nil,err
	}
	defer file.Close()
	content,err := io.ReadAll(file)
	if (err != nil){
		return nil,err
	}
	return content,nil
}

func ReadAsStream (path string)(ret *os.File,err error)  {
	file,err := os.Open(path)
	if(err != nil){
		return nil,err	
	}
	return file,nil
}