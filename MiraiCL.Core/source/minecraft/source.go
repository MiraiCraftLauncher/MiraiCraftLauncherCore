package minecraft

type Source struct{
	VersionIndex string
	VersionIndexV2 string
	MavenServer string
	ResourceServer string
	JavaIndex string

}

var Mojang = Source{
	VersionIndex: "https://piston-meta.mojang.com/mc/game/version_manifest.json",
	VersionIndexV2: "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json",
	MavenServer: "https://libraries.minecraft.net",
	ResourceServer: "https://resources.download.minecraft.net",
	JavaIndex: "https://piston-meta.mojang.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json",
}

var BMCLAPI = Source{
	VersionIndex: "https://bmclapi2.bangbang93.com/mc/game/version_manifest.json",
	VersionIndexV2: "https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json",
	MavenServer: "https://bmclapi2.bangbang93.com/maven",
	ResourceServer: "https://bmclapi2.bangbang93.com/assets",
	JavaIndex: "https://bmclapi2.bangbang93.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json",
}

var customSource []Source = nil