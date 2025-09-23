package minecraft

import (
	"encoding/json"
	"github.com/MiraiCL/MiraiCL.Core/base/net"
	"github.com/MiraiCL/MiraiCL.Core/models/minecraft"
)

var versionIndex minecraft.VersionList

func VersionIndex() error {
	resp,err := net.NewHttpRequestBuilder("","").Execute()
	if err != nil {
		return err
	};
	var data []byte
	_,err = resp.Body.Read(data)
	if err != nil{
		return err
	};
	
	err = json.Unmarshal(data,&versionIndex)
	if err != nil{
		return err
	};
	return nil
}

func ReadVersionInfo(version string) *minecraft.Version{
	if version == nil {
		VersionIndex()
	}
	for _,v := range versionIndex.Versions{
		if v.Id ==
	}	
}