package helper

import(
	"crypto"
	"github.com/MiraiCL/MiraiCL.Core/base"
	"io"
	"encoding/hex"
)

func MD5File(path string)(ret string,err error){
	md5 := crypto.MD5.New()
	file,err := base.ReadAsStream(path)
	if err != nil{
		return "",err
	}
	defer file.Close()
	if _,err := io.Copy(md5,file);err != nil{
		return "",nil
	}
	return hex.EncodeToString(md5.Sum(nil)),nil
}

func SHA1File(path string)(ret string,err error){
	sha1 := crypto.SHA1.New()
	file,err := base.ReadAsStream(path)
	if err != nil{
		return "",err
	}
	defer file.Close()
	if _,err := io.Copy(sha1,file); err != nil{
		return "",err
	}
	return hex.EncodeToString(sha1.Sum(nil)),nil
}

func SHA256File(path string)(ret string,err error){
	sha256 := crypto.SHA256.New()
	file,err := base.ReadAsStream(path)
	if err != nil{
		return "",err
	}
	defer file.Close()
	if _,err := io.Copy(sha256,file); err != nil{
		return "",err
	}
	return hex.EncodeToString(sha256.Sum(nil)),nil
}

func SHA512File(path string)(ret string,err error){
	sha512 := crypto.SHA512.New()
	file,err := base.ReadAsStream(path)
	if err != nil{
		return "",err
	}
	defer file.Close()
	if _,err := io.Copy(sha512,file); err != nil{
		return "",err
	}
	return hex.EncodeToString(sha512.Sum(nil)),nil
}

func MurmurHash2(path string)(ret uint32,err error){
	file,err := base.ReadAsStream(path)
	if err != nil{
		return 0,nil
	};
	byteList := make([]byte,16384)
}