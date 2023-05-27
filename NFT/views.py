from django.shortcuts import render, redirect
import requests
import json
import random
import math
from django.http import JsonResponse
"""
const CaverExtKAS = require("caver-js-ext-kas");
const originalCaver_ = require("caver-js");
const originalCaver = new originalCaver_(
  "https://public-en-baobab.klaytn.net/"
);

// 1001이 testnet, 8217이 mainnet
const chainId = 1001;
const accessKeyId = "KASKHT32FUV2LSVC00OZ2DHM";
const secretAccessKey = "XM-hoBODxZCZdpgvJqeWl7LdG2JpGX4Ny5YB16Qa";
// const privateKey = "krn:1001:wallet:56ba73e4-b905-4cf2-aa8f-c4ec16d68430:account-pool:default:0xac0e6499769d8ab6d850cbde1dd341f767c6cfe96fb247be204aa708135d91e5";
const privateKey =
  "0xac0e6499769d8ab6d850cbde1dd341f767c6cfe96fb247be204aa708135d91e5";
const caver = new CaverExtKAS(chainId, accessKeyId, secretAccessKey);
// import { initializeApp } from "firebase/app";
const firebaseApp = require("firebase/app");

const firestore = require("firebase/firestore");

const firebaseConfig = {
  apiKey: "AIzaSyDU3nlY60-dxU8V03ywgYUYRXhDuIcBoHs",
  authDomain: "animalnft-98485.firebaseapp.com",
  projectId: "animalnft-98485",
  storageBucket: "animalnft-98485.appspot.com",
  messagingSenderId: "5720138965",
  appId: "1:5720138965:web:26742ba28dc1d30a06ee5c",
  measurementId: "G-EWWWYY4G3B",
};

const app = firebaseApp.initializeApp(firebaseConfig);

const db = firestore.getFirestore(app);

const generateWallet = async (data, context) => {
  const result = await caver.kas.wallet.createAccount();
  console.log(result);
  /* result =>
  Account {
  address: '0x09634F250DeAaA20d0F93da624662eB5339E6212',
  chainId: 1001,
  createdAt: 1601970606,
  keyId: 'krn:1001:wallet:8e76d003-d6dd-4278-8d05-5172d8f010ca:account-pool:default:0xc8bca3c1f9e09d4f38b6a629f27fff9cab3ead3ddf3791c2df01d9f0d8b743f2',
  krn: 'krn:1001:wallet:8e76d003-d6dd-4278-8d05-5172d8f010ca:account-pool:default',
  publicKey: '0x04df8709251407a1663432ae0e0f21291b9d6ec01ad656773a56b951ebcc56c65323f4dfe7141ce71a6350f7186f6150db8833f30be357cc8bb4d416a9f5402548',
  updatedAt: 1601970606
}
  */
  try {
    const walletRef = await firestore.setDoc(
      firestore.doc(db, "NFT_wallet", data.ID),
      {
        // TODO data
        userID: data.ID,
        address: result.address,
        chainId: result.chainId,
        createdAt: result.createdAt,
        privateKey: result.keyId,
        krn: result.krn,
        publicKey: result.publicKey,
      }
    );
    console.log("Wallet written with ID to firestore: ", data.ID);
    // console.log("Wallet Ref: ", walletRef);
  } catch (e) {
    console.error("Error adding wallet to firestore: ", e);
  }

  return result;
};
const registerContract = async (data, context) => {
  const keyring = originalCaver.wallet.keyring.createFromPrivateKey(privateKey);
  if (!originalCaver.wallet.getKeyring(keyring.address)) {
    const singleKeyRing = caver.wallet.keyring.createFromPrivateKey(privateKey);
    originalCaver.wallet.add(singleKeyRing);
  }
  var contractAddr = "";
  try {
    const kip17 = await caver.kas.kip17
      .deploy(
        "Animal NFT KAIST",
        "ANI",
        "animal-ntf-kaist5"

        // keyring.address
      )
      .then((kip17) => {
        console.log(kip17);
        contractAddr = kip17.transactionHash;
      });
  } catch (e) {
    console.log(e);
  }
  if (contractAddr == "") return;

  // console.log()
  try {
    const walletRef = await firestore.setDoc(
      firestore.doc(db, "NFT_contract", data.ID),
      {
        // TODO data
        userID: data.ID,
        contractAddr: contractAddr,
        registeredDate: firestore.serverTimestamp(),
      }
    );
    console.log("contract written with ID to firestore: ", data.ID);
  } catch (e) {
    console.error("Error adding contract to firestore: ", e);
  }
  // return;
};

const mintToken = async (data, context) => {
  const keyring = caver.wallet.keyring.createFromPrivateKey(privateKey);
  if (!originalCaver.wallet.getKeyring(keyring.address)) {
    const singleKeyRing = caver.wallet.keyring.createFromPrivateKey(privateKey);
    originalCaver.wallet.add(singleKeyRing);
  }
  //TODO data.ID
  const contractsRef = firestore.doc(db, "NFT_contract", data.userID);
  const contractsSnap = await firestore.getDoc(contractsRef);
  // var contractData = "";
  if (contractsSnap.exists()) {
    console.log("Contract data:", contractsSnap.data());
    // const contractData = contractsSnap.data();
  } else {
    // docSnap.data() will be undefined in this case
    console.log("No such contract!");
  }
  // if (contractData == "") return;
  // console.log("hihi");
  // console.log(contractsSnap.data());
  // const kip17 = new caver.kct.kip17(
  //    contractsSnap.data().contractAddr
  // );

  minted = false;
  // console.log("This is keyring addr: ", keyring.address);
  // console.log(userWalletAddr.body);
  // console.log(typeof randomID);
  // console.log(typeof imgURI);
  // console.log(typeof keyring.address);

  randomID = Math.floor(Math.random() * Number.MAX_SAFE_INTEGER);
  console.log("randomID", randomID);
  try {
    // console.log("we can mint");

    mintResult = await caver.kas.kip17.mint(
      "animal-ntf-kaist5",
      data.userWalletAddr,
      randomID,
      data.imgURI
    );
    try {
      const tokenRef = await firestore.updateDoc(
        firestore.doc(db, "NFT_contract", data.userID),
        {
          // TODO data
          // userID: data.ID,
          // contractAddr: contractAddr,
          tokenID: randomID,
          tokenURI: data.imgURI,
          fromAddr: keyring.address,
          toAddr: data.userWalletAddr,
          updateDate: firestore.serverTimestamp(),
        }
      );
      console.log("Token info to firestore: ", data.userID);
      minted = true;
    } catch (e) {
      console.error("Error adding token to firestore: ", e);
    }
  } catch (e) {
    console.log(e);
  }
};
const sendToken = () => {};

module.exports = {
  generateWallet,
  registerContract,
  mintToken,
  sendToken,
};
"""

chain_id = 1001
access_key_id = "KASKHT32FUV2LSVC00OZ2DHM";
secret_access_key = "XM-hoBODxZCZdpgvJqeWl7LdG2JpGX4Ny5YB16Qa";
account_pool_krn = "krn:8217:wallet:56ba73e4-b905-4cf2-aa8f-c4ec16d68430:account-pool:AnimalNFT"
# Create your views here.
def create_wallet(request) : 
  global chain_id, access_key_id, secret_access_key
  if request.method=='POST' :
    headers = {
      'x-chain-id': {chain_id},
      'x-krn':{account_pool_krn}
    }
    response = requests.post('https://wallet-api.klaytnapi.com/v2/account', headers=headers, auth=(access_key_id, secret_access_key))
    # print(response.json())
    return JsonResponse(response.json())
  else :
    pass
  context = {
  }
  return render(request, 'single_pages/login.html', context)

# def register_contract(request):
#   global chain_id, access_key_id, secret_access_key
#   headers = {
#     'x-chain-id': chain_id,
#     'content-type': 'application/x-www-form-urlencoded',
#   }

#   data = {"alias": "animal-ntf-kaist6", "name": "Animal NFT KAIST", "symbol": "ANI"  }

#   response = requests.post('https://kip17-api.klaytnapi.com/v2/contract', headers=headers, data=data, auth=(access_key_id, secret_access_key))
#   print(response.json())
    
def mint_token(request):
      
  print(request.POST)
  print(request.FILES)
  
  #save image into IPFS via NFT.storage
  files = {
    'image': open('image.jpg', 'rb'),
    'meta': (None, '{"image":null,"name":"AnimalNFT","description":id_YYYYMMDD,"properties":{}}'),
  }

  response = requests.post('https://api.nft.storage/store', files=files)
  if not response.status_code ==200:
    return render(request, 'gallery:post_list')

  IPFS_data = response.json()
  token_uri = "ipfs.io/ipfs/" + IPFS_data.value.cid


  #klaytn token minting
  global chain_id, access_key_id, secret_access_key
  data = request.POST
  headers = {
    'x-chain-id': chain_id,
    'content-type': 'application/x-www-form-urlencoded',
  }
  randomID = math.random()
  data = {"to": request.user.wallet, "id": randomID, "uri": token_uri}
  
  response = requests.post('https://kip17-api.klaytnapi.com/v2/contract/animal-ntf-kaist5/token', headers=headers, data=data, auth=(access_key_id, secret_access_key))
  return render(request, 'gallery:post_list')
