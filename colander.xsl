<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:ditaarch="http://dita.oasis-open.org/architecture/2005/" >

    <xsl:strip-space elements="*"/>
    <xsl:output method="xhtml" encoding="UTF-8" indent="yes" omit-xml-declaration="yes" />

    <!-- <xsl:template match="@*|node()">
        <xsl:copy inherit-namespaces="no" copy-namespaces="no">
            <xsl:apply-templates select="@*|node()" />
        </xsl:copy>
    </xsl:template> -->

    <xsl:template match="/topic">
        <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html&gt;</xsl:text>
        <html>
            <xsl:apply-templates select="@*" />
            <head>
                <link rel="stylesheet" href="../preview.css" />
            </head>
            <xsl:apply-templates select="node()" />
        </html>
    </xsl:template>
    
    <!-- <xsl:template match="title">
        <xsl:choose>
            <xsl:when test="following-sibling::*[1][name()='body']">
            </xsl:when>
            
            <xsl:otherwise>
                <h1>
                    <xsl:apply-templates select="@*|node()" />
                </h1>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template> -->
    
    <!-- <xsl:template match="body">
        <xsl:copy>
            <xsl:apply-templates select="@*" />
            
            <xsl:for-each select="preceding-sibling::*[1][local-name()='title']">
                <h1>
                    <xsl:apply-templates select="@*" />
                    <xsl:for-each select="node()">
                        <xsl:choose>
                            <xsl:when test="self::indexterm">
                                
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:copy>
                                    <xsl:apply-templates select="@*|node()" />
                                </xsl:copy>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:for-each>
                </h1>
            </xsl:for-each>
            
            <xsl:apply-templates select="node()" />
        </xsl:copy>
    </xsl:template> -->
    
    <xsl:template match="sl">
        <ol>
            <xsl:for-each select="sli">
                <li>
                    <xsl:apply-templates select="@*|node()" />
                </li>
            </xsl:for-each>
        </ol>
    </xsl:template>


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

    <!-- <xsl:template match="@otherprops">
        <xsl:attribute name="class">
            <xsl:value-of select="if (parent::*/@class) then normalize-space(concat(parent::*/@class, ' ', .)) else ." />
        </xsl:attribute>
    </xsl:template>
     -->

    <!-- <xsl:template match="fig">
        <xsl:for-each-group select="*" group-ending-with="*[preceding-sibling::*[1][name()='image'][not(preceding-sibling::*)]]">
            <xsl:choose>
                <xsl:when test="current-group()[preceding-sibling::*[1][name()='image'][not(preceding-sibling::*)]]">
                    <div>
                        <xsl:attribute name="class" select="'figure'" />
                        <xsl:apply-templates select="current-group()" />
                    </div>
                </xsl:when>
                
                <xsl:otherwise>
                    <xsl:apply-templates select="current-group()" />
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each-group>
    </xsl:template> -->
    
    <xsl:template match="figgroup">
        <div>
            <xsl:attribute name="class" select="'figgroup'" />
            <xsl:apply-templates select="@*|node()" />
        </div>
        
    </xsl:template>
    
    <xsl:template match="xref">
        <a href="{@href}">
            <xsl:value-of select="@href"/>
        </a>
    </xsl:template>

    <xsl:template match="image[@placement='inline']">
        <img height='24px'>
            <xsl:attribute name="src">
                <xsl:value-of select="@href" />
            </xsl:attribute>
        </img>
    </xsl:template>

    <xsl:template match="image[@placement='break']">
        <img width='80%'>
            <xsl:attribute name="src">
                <xsl:value-of select="@href" />
            </xsl:attribute>
            <xsl:attribute name="max-width">
                '800px'
            </xsl:attribute>
        </img>
    </xsl:template>

    <!-- <xsl:template match="image">
        <img width='90%'>
            <xsl:attribute name="src">
                <xsl:value-of select="@href" />
            </xsl:attribute>
        </img>
    </xsl:template> -->

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" />
        </xsl:copy>
    </xsl:template>

    <!-- <xsl:template match="@ditaarch:DITAArchVersion | @domains | @class"> </xsl:template> -->

</xsl:stylesheet>
