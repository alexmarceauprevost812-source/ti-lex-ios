import {mkdir,copyFile,readdir} from "node:fs/promises";
import path from "node:path";
const root=process.cwd();
await mkdir(path.join(root,"public/assets"),{recursive:true});
for(const name of ["index.html","style.css","app.js"])await copyFile(path.join(root,"preview",name),path.join(root,"public",name));
const assets=path.join(root,"debian13/config/includes.chroot/usr/share/ti-lex/branding");
for(const name of await readdir(assets))if(/\.(png|svg)$/.test(name))await copyFile(path.join(assets,name),path.join(root,"public/assets",name));
console.log("Aperçu généré dans public.");
