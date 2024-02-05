<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:ditaarch="http://dita.oasis-open.org/architecture/2005/" >

    <xsl:strip-space elements="*"/>
    <xsl:output method="html" encoding="UTF-8" indent="yes" omit-xml-declaration="yes" />

    <xsl:template match="/topic">
        <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html&gt;</xsl:text>
        <html>
            <xsl:apply-templates select="@*" />
            <head>
                <link rel="stylesheet" href="../preview.css" />
            </head>
            <body>
                <!-- <xsl:apply-templates select="node()" /> -->
                <xsl:apply-templates />
            </body>
        </html>
    </xsl:template>
   
<!-- topic -->

    <xsl:template match="topic/title">
        <h1>
            <xsl:apply-templates />
        </h1>
    </xsl:template>

    <xsl:template match="topic/topic/title">
        <h2>
            <xsl:apply-templates />
        </h2>
    </xsl:template>

    <xsl:template match="section/title">
        <h3>
            <xsl:apply-templates />
        </h3>
    </xsl:template>    
    
    <xsl:template match="p[@otherprops='subsection']">
        <h4>
            <xsl:apply-templates/>
        </h4>
    </xsl:template>

    <xsl:template match="p[@otherprops='subsubsection']">
        <h5>
            <xsl:apply-templates/>
        </h5>
    </xsl:template>

    <xsl:template match="sectiondiv">
        <xsl:apply-templates />
    </xsl:template>
    
    <xsl:template match="section">
        <xsl:apply-templates />
    </xsl:template>

    <xsl:template match="body">
        <xsl:apply-templates />
    </xsl:template>

    <xsl:template match="topic/topic">
        <xsl:apply-templates />
    </xsl:template>

<!-- cross-reference -->

    <xsl:template match="xref">
        <a href="{@href}">
            <xsl:value-of select="@href"/>
        </a>
    </xsl:template>

<!-- image -->

    <xsl:template match="image[@placement='inline']">
        <img height='36px'>
            <xsl:attribute name="src">
                <xsl:value-of select="@href" />
            </xsl:attribute>
        </img>
    </xsl:template>

    <xsl:template match="image">
        <img width='80%'>
            <xsl:attribute name="src">
                <xsl:value-of select="@href" />
            </xsl:attribute>
        </img>
    </xsl:template>

<!-- list  -->

    <xsl:template match="sl">
        <ol>
            <xsl:for-each select="sli">
                <li>
                    <xsl:apply-templates select="@*|node()" />
                </li>
            </xsl:for-each>
        </ol>
    </xsl:template>

<!-- table -->

<!-- Matches any other DITA element and copies it as is -->
    <!-- <xsl:template match="*"> -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" />
        </xsl:copy>
    </xsl:template>

    <!-- <xsl:template match="@ditaarch:DITAArchVersion | @domains | @class"> </xsl:template> -->

</xsl:stylesheet>
